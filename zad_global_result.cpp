#include <iostream>
#include <vector>
using namespace std;

std::vector<vector<int>> results;
std::vector<int> result;
std::vector<int> primes;


bool is_prime(int number)
{   
    if(number < 2) return false;
    for(int i = 2; i*i <= number; i++)
    {
        if(number % i == 0) return false;
    }
    return true;
}

void list_primes(int number)
{
    primes.push_back(2);
    for(int i = 3; i <= number; i += 2) 
    {
        if(is_prime(i)) primes.push_back(i);
    }
}

void calculate_results(int number, int imax)
{
    for (int i = imax; i >= 0; i--) 
    {  
        int diff = number - primes[i];
        bool remove = false;

        if(diff > 1)
        {
            result[i] += 1;
            calculate_results(diff, i);
            diff += primes[i];
            remove = true;
        }
        if(diff == 0) 
        {   
            result[i] += 1;
            results.push_back(result);
            remove = true;
        }
        if(remove) result[i] -= 1;
     } 
}

int main() 
{
    int inputs = 0;
    cin >> inputs;


    for (int i = 0; i < inputs; i++) 
    {
        int n, k;
        cin >> n >> k;

        int limit = ((n - k) < k) ? n - k: k;
        if (is_prime(k) && limit > -1)
        {
            if(n == k) {
                cout << k << endl;
            }
            else 
            {
                list_primes(limit);

                result.assign(primes.size(), 0);
                calculate_results(n - k,  primes.size() - 1);
                
                // display results
                for(int r = results.size() - 1; r > -1; r--)
                {
                    cout << k;
                    for (int d = results[r].size() - 1; d > -1; d--)
                    {
                        int index = results[r][d];
                        while(index > 0) {
                            cout << "+" << primes[d];
                            index--;
                        }
                    } 
                    cout << endl;
                }

                // cleanup
                results.clear();
                result.clear();
                primes.clear();
            }
        }
    }
     return 0;
}

 #include <iostream>
 using namespace std;
 void tower(int N, int a, int b, int c)
 {
    if(N == 1)
    {
    cout << a << " ---> " << c <<endl;
    return;
    }    
    tower(N - 1, a, c, b); 
    tower(1, a, b, c); 
    tower(N - 1, b, a, c);
 }
 int main()
 {
 int N;
 cin >> N;
 int a = 1, b = 2, c = 3;
 tower(N, a, b, c); 
}
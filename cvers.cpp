#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int Eval(int n, int *s, int *c)
{
    int i, j, totc = 0;
    for (i = 0; i < n; i++)
        c[i] = 0;
    for (i = 0; i < n - 1; i++)
    {
        for (j = i + 1; j < n; j++)
        {
            if (s[i] == s[j])
            {
                c[i]++;
                c[j]++;
                totc++;
            }
            else if (abs(s[i] - s[j]) == abs(i - j))
            {
                c[i]++;
                c[j]++;
                totc++;
            }
        }
    }
    return totc;
}
int HillClimbNQueens(int n, int *s, int MaxIterations, int *restarts, int step)
{
    int val, i, j, qi, qj, min, temp;
    int *c, u[n], tempc[n][n];
    *restarts = 0;
    if (step > n)
        step -= n;
    for (i = 0; i < n; i++)
        s[i] = rand() % n;
    val = Eval(n, s, c = &(tempc[0][0]));
    while (MaxIterations-- > 0)
    {
        if (val == 0)
            return MaxIterations;
        do
            qi = rand() % n;
        while (c[qi] == 0);
        min = val;
        qj = -1;
        for (j = 0; j < n; j++)
        {
            s[qi] = j;
            temp = Eval(n, s, &(tempc[j][0]));
            if (temp < min)
            {
                min = temp;
                qj = 0;
                u[qj] = j;
            }
            else if (temp == min)
            {
                qj++;
                u[qj] = j;
            }
        }
        if (qj >= 0)
        {
#ifdef BADCHOICEs[qi] = u[0];
#elseif(qj > 0) qj = rand() % (qj + 1);
            s[qi] = u[qj];
#endifval = min;
            c = &(tempc[u[qj]][0]);
        }
    }
    return 0;
}
int main(int argc, char *argv[])
{
    int n = 10, maxit = 1000, seed, step = 1;
    if (argc > 1)
        n = atoi(argv[1]);
    if (argc > 2)
        seed = atoi(argv[2]);
    else
        seed = time(0);
    if (argc > 3)
        maxit = atoi(argv[3]);
    if (argc > 4)
        step = atoi(argv[4]);
    srand(seed);
    int s[n];
    int i;
    for (i = 0; i < n; i++)
        s[i] = rand() % n;
    int restarts;
    int tempit = maxit - HillClimbNQueens(n, s, maxit, &restarts, step);
    if (tempit < maxit)
    {
        printf("%d\t%d\t%d\t%d\t0\n", n, step, tempit, restarts);
    }
    else
    {
        int c[n];
        printf("%d\t%d\t%d\t%d\t%d\n", n, step, maxit - tempit, restarts, Eval(n, s, c));
    }
    return 0;
}
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <ctime> // time_t
#include <cstdio>

using namespace std;

struct Tile
{
    int row;
    int col;

    Tile(int x, int y)
    {
        this->row = x;
        this->col = y;
    }
};

class NQueens
{

private:
    int n;
    int *positions;
    int *row;
    int *mdiag;
    int *sdiag;
    int conflicts;

public:
    NQueens(int n)
    {
        srand(time(NULL));
        this->n = n;

        this->setBoard(n);
        this->conflicts = this->getConflicts();
    }

    void setBoard(int n)
    {
        this->positions = new int[n + 1];
        this->row = new int[n + 1];
        this->mdiag = new int[n * 2 + 1];
        this->sdiag = new int[n * 2 + 1];
        for (int i = 0; i < 2 * n; i++)
        {
            if (i <= n)
            {
                this->row[0] = 0;
            }
            this->mdiag[i] = 0;
            this->sdiag[i] = 0;
        }
        for (int i = 1; i < n + 1; i++)
        {
            int j = rand() % n + 1;
            this->positions[i] = j;
            this->row[j]++;
            this->mdiag[j + i]++;
            this->sdiag[n - j + 1 + i]++;
        }
    }

    int getConflicts()
    {
        int conflicts = 0;
        for (int i = 1; i < this->n * 2 + 1; i++)
        {
            int x = (i <= this->n) ? this->row[i] : 0;
            int y = this->mdiag[i];
            int z = this->sdiag[i];
            conflicts += (x * (x - 1)) / 2;
            conflicts += (y * (y - 1)) / 2;
            conflicts += (z * (z - 1)) / 2;
        }
        return conflicts;
    }

    int getAllQueenConflicts(int row, int col)
    {
        return this->row[row] + this->mdiag[row + col] + this->sdiag[n + col - 1 - row] - 3;
    }

    bool hasConflicts()
    {
        return this->conflicts > 0;
    }

    void solve()
    {
        int counter = 0;
        while (this->hasConflicts())
        {
            int minAttacks = this->n + 1;
            int col = rand() % n + 1;
            int row = this->positions[col];
            Tile best(0, 0);
            Tile pos(row, col);
            for (int i = 1; i < this->n + 1; i++)
            {
                Tile newPos(i, col);
                this->move(pos, newPos);
                int conflicts = this->getAllQueenConflicts(i, col);
                if (conflicts < minAttacks)
                {
                    best.row = i;
                    best.col = col;
                    minAttacks = conflicts;
                }
                this->move(newPos, pos);
            }
            this->move(pos, best);
            if (best.row == pos.row && best.col == pos.col)
            {
                counter++;
            }
            if (counter >= 10000)
            {
                counter = 0;
                this->setBoard(this->n);
            }
        }
    }

    void move(Tile pos, Tile newPos)
    {
        this->conflicts -= this->getAllQueenConflicts(pos.row, pos.col);
        this->positions[pos.col] = newPos.row;
        this->row[pos.row]--;
        this->row[newPos.row]++;
        this->mdiag[pos.row + pos.col]--;
        this->mdiag[newPos.row + newPos.col]++;
        this->sdiag[this->n + newPos.col + 1 - newPos.row]++;
        this->sdiag[this->n + pos.col + 1 - pos.row]--;
        this->conflicts += this->getAllQueenConflicts(newPos.row, newPos.col);
    }

    void print()
    {
        int **board = new int *[n];
    
        for (int i = 0; i < n; i++)
        {
            board[i] = new int[n];
        }
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                board[i][j] = 0;
            }
        }
        for (int i = 1; i < this->n + 1; i++)
        {
            board[this->n - this->positions[i]][i - 1] = 1;
        }
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                cout << board[i][j];
            }
            cout << endl;
        }
    }
};

int main()
{
    cout<<"Enter n :"<<endl;
    int n;
    cin >> n;
    NQueens nq(n);
    time_t begin, end;

    time(&begin);
    nq.solve();
    time(&end);

    double difference = difftime(end, begin);
    printf("time taken for solving n queens was %.2lf seconds.\n", difference);
    
    int print;
    cout<<"Enter 1 to print the grid"<<endl;
    cin >> print;
    if(print == 1){
        nq.print();
    }
}
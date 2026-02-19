#include <iostream>
#include <vector>

#define INDEX(x, y, n) ((y) * (n) + (x))

struct SquareDate{
    int x, y, size;
};

class Square{
private:
    int n;
    int cnt_squares{0};
    std::vector<int> field;
    std::vector<SquareDate> squares;

    int min_cnt_squares;
    std::vector<SquareDate> best_squares;

    int area;

    bool can_place(int x, int y, int size){
        if (x + size > n || y + size > n) return false;

        for(int yi = y; yi < y + size; yi++){
            for(int xi = x; xi < x + size; xi++){
                if(field[INDEX(xi, yi, n)]) return false;
            }
        }
        return true;
    }

    void place_square(int x, int y, int size, int value){
        int delta = size * size;

        for (int yi = y; yi < y + size; yi++){
            for (int xi = x; xi < x + size; xi++){
                field[INDEX(xi, yi, n)] = value;
            }
        }

        if (value){
            cnt_squares++;
            area -= delta;
        } else {
            cnt_squares--;
            area += delta;
        }
    }

    void find_first_coord(int start_y, int& new_x, int& new_y){
        for (int yi = start_y; yi < n; yi++){
            for (int xi = 0; xi < n; xi++){
                if (!field[INDEX(xi, yi, n)]){
                    new_x = xi;
                    new_y = yi;
                    return;
                }
            }
        }
        new_x = new_y = -1;
    }

    void backtrace(int y){
        if (cnt_squares >= min_cnt_squares){
            return;
        }
        if (area == 0) {
            if (cnt_squares < min_cnt_squares){
                min_cnt_squares = cnt_squares;
                best_squares = squares;
                //std::cout << "Решние с " << cnt_squares << " квадратами" << std::endl;
            }
            return;
        };

        int next_x, next_y;
        find_first_coord(y, next_x, next_y);

        int max_s = std::min(n - next_x, n - next_y);
        int min_s = 1;
        if (cnt_squares == 0) {
            max_s = n - 1;
            min_s = (n + 1) / 2;
        }

        for (int size = max_s; size >= min_s; size--){
            if (can_place(next_x, next_y, size)){
                place_square(next_x, next_y, size, 1);
                squares.push_back(SquareDate{next_x + 1, next_y + 1, size});

                backtrace(next_y);

                place_square(next_x, next_y, size, 0);
                squares.pop_back();
            }
        }
    }

public:
    Square(int n) : n(n) {
        field.assign(n * n, 0);
        min_cnt_squares = n * n + 1;
        area = n * n;

        backtrace(0);
    };

    int get_cnt_squares() {return min_cnt_squares;};
    std::vector<SquareDate> get_squares() {return best_squares;};
};


int main(){
    int n;
    std::cin >> n;

    Square s(n);

    std::cout << s.get_cnt_squares() << std::endl;

    auto res = s.get_squares();
    for (auto& sq : res){
        std::cout << sq.x << " " << sq.y << " " << sq.size << std::endl;
    }

    return 0;
}
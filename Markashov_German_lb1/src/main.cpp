#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>

using namespace std::chrono;

#define DEBUG false
#define COLLECT_DATA false
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

    long long cnt_ops{0};

    std::string indent(int depth){
        return std::string(depth * 2, ' ');
    }

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

    void backtrace(int y, int depth){
        cnt_ops++;
        if (cnt_squares >= min_cnt_squares - 1 && area > 0){
            if (DEBUG) std::cout << indent(depth)
                << "- Текущее решение хуже лучшего, возвращяюсь на этап назад..." << std::endl;
            return;
        }
        if (area == 0) {
            if (cnt_squares < min_cnt_squares){
                min_cnt_squares = cnt_squares;
                best_squares = squares;
                if (DEBUG) std::cout << "\n" << indent(depth) << ">>> Найдено решение: "
                    << cnt_squares << " квадратов" << " <<<\n" << std::endl;
            }
            return;
        };

        int next_x, next_y;
        find_first_coord(y, next_x, next_y);
        if (next_x == -1) return;

        int max_s = std::min(n - next_x, n - next_y);

        for (int size = max_s; size >= 1; size--){
            if (can_place(next_x, next_y, size)){
                if (DEBUG) std::cout << indent(depth) << "+ Пробуем " << size << "x" << size 
                    << " в точку (" << next_x << "," << next_y << ")\n";

                place_square(next_x, next_y, size, 1);
                squares.push_back(SquareDate{next_x + 1, next_y + 1, size});

                backtrace(next_y, depth + 1);

                place_square(next_x, next_y, size, 0);
                squares.pop_back();
            }
        }
    }

public:
    Square(int n) : n(n) {
        if (n % 2 == 0){
            cnt_ops++;
            int size = n / 2;
            best_squares.push_back(SquareDate({1, 1, size}));
            best_squares.push_back(SquareDate({1 + size, 1, size}));
            best_squares.push_back(SquareDate({1, 1 + size, size}));
            best_squares.push_back(SquareDate({1 + size, 1 + size, size}));
            min_cnt_squares = 4;
            return;
        }

        field.assign(n * n, 0);
        min_cnt_squares = n * n + 1;
        area = n * n;

        for(int size = n - 1; size >= (n + 1) / 2; size--){
            place_square(0, 0, size, 1);
            squares.push_back({1, 1, size});

            backtrace(0, 1);

            place_square(0, 0, size, 0);
            squares.pop_back();
        }
    };

    int get_cnt_squares() {return min_cnt_squares;};
    std::vector<SquareDate> get_squares() {return best_squares;};
    int get_cnt_ops() {return cnt_ops;};

    void draw_square(){
        std::vector<std::vector<int>> matrix;
        matrix.resize(n);
        for (int y = 0; y < n; y++){
            matrix[y].assign(n, 0);
        }

        for (int i = 0; i < best_squares.size(); i++){
            int x = best_squares[i].x - 1;
            int y = best_squares[i].y - 1;
            int size = best_squares[i].size;
            for (int yi = y; yi < y + size; yi++){
                for (int xi = x; xi < x + size; xi++){
                    matrix[yi][xi] = i;
                }
            }
        }

        for (int y = 0; y < n; y++){
            for (int x = 0; x < n; x++){
                std::cout << matrix[y][x] << " ";
            }
            std::cout << std::endl;
        }
    }
};

void collect_data(int n){
    std::ofstream file("data.csv");

    if (file.is_open()){
        file << "n,cnt_ops,time" << std::endl;

        for(int ni = 2; ni < n; ni++){
            auto start = high_resolution_clock::now();
            Square s(ni);
            auto stop = high_resolution_clock::now();

            auto duration = duration_cast<microseconds>(stop - start);
            file << ni << "," << s.get_cnt_ops() << "," << duration.count() / 1000000 << '.' << duration.count() % 1000000 << std::endl;

        }
    file.close();
    }
}

int main(){
    int n;

    if (DEBUG) std::cout << "Введите N (размер квадрата): ";
    std::cin >> n;

    if (n < 2){
        return 1;
    }

    auto start = high_resolution_clock::now();
    Square s(n);
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(stop - start);
    std::cout << duration.count() / 1000000 << '.' << duration.count() % 1000000 << std::endl;

    if (DEBUG) std::cout << "Кол-во операций вставки квадратов: " << s.get_cnt_ops() << std::endl;

    if (DEBUG) std::cout << "Минимальное кол-во квдаратов из которых можно собрать большой квадрат: ";
    std::cout << s.get_cnt_squares() << std::endl;

    if (DEBUG) std::cout << "X | Y | SIZE" << std::endl;
    auto res = s.get_squares();
    for (auto& sq : res){
        std::cout << sq.x << " " << sq.y << " " << sq.size << std::endl;
    }

    if (DEBUG) std::cout << "\nВизуализация: " << std::endl;
    if (DEBUG) s.draw_square();

    if (COLLECT_DATA) collect_data(21);

    return 0;
}

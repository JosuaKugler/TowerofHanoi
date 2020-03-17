#include "TowerOfHanoi.hh"

TowerOfHanoi::TowerOfHanoi(int n, int k) {
    _n = n;
    _k = k;
    _config = new int[_n];
    for (size_t i = 0; i < n; i++)
    {
        _config[i] = 0;
    }
}

TowerOfHanoi::TowerOfHanoi(int n, int k, int* config) {
    _n = n;
    _k = k;
    _config = config;
}

TowerOfHanoi::TowerOfHanoi(TowerOfHanoi& tower) {
    _n = tower._n;
    _k = tower._k;
    _config = new int[_n];
    for (size_t i = 0; i < _n; i++)
    {
        _config[i] = tower._config[i];
    }
}

TowerOfHanoi::~TowerOfHanoi() {
    delete _config;
}

bool TowerOfHanoi::move(Move move) {
    int origin = _config[move.disk];
    for (size_t i = 0; i < move.disk; i++)
    {
        if (_config[i] == origin or _config[i] == move.destination)
        {
            return false;
        }
    }
    _config[move.disk] = move.destination;
    return true;
}
bool TowerOfHanoi::move(FullMove move) {
    int origin = move.origin;
    for (size_t i = 0; i < move.disk; i++)
    {
        if (_config[i] == origin or _config[i] == move.destination)
        {
            return false;
        }
    }
    _config[move.disk] = move.destination;
    return true;
}

bool TowerOfHanoi::move(int disk, int destination) {
    int origin = _config[disk];
    for (size_t i = 0; i < disk; i++)
    {
        if (_config[i] == origin or _config[i] == destination)
        {
            return false;
        }
    }
    _config[disk] = destination;
    return true;
}
/*
  Based on Jean-Francois Romang work from
  https://github.com/jromang/Stockfish/blob/pyfish/src/pyfish.cpp
*/

#include <Python.h>

#include "misc.h"
#include "types.h"
#include "bitboard.h"
#include "evaluate.h"
#include "notation.h"
#include "position.h"
#include "search.h"
#include "syzygy/tbprobe.h"
#include "thread.h"
#include "tt.h"
#include "uci.h"

static PyObject* PySFishError;

namespace PSQT {
  void init();
}

using namespace std;

namespace
{
// FEN string of the initial position
const char* StartFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[HEhe] w KQBCDFGkqbcdfg - 0 1";
}

extern "C" PyObject* pysfish_info(PyObject* self) {
    return Py_BuildValue("s", engine_info().c_str());
}

// INPUT option name, option value
extern "C" PyObject* pysfish_setOption(PyObject* self, PyObject *args) {
    const char *name;
    PyObject *valueObj;
    if (!PyArg_ParseTuple(args, "sO", &name, &valueObj)) return NULL;

    if (Options.count(name))
        Options[name] = string(PyBytes_AS_STRING(PyUnicode_AsEncodedString(PyObject_Str(valueObj), "UTF-8", "strict")));
    else
    {
        PyErr_SetString(PyExc_ValueError, (string("No such option ")+name+"'").c_str());
        return NULL;
    }
    Py_RETURN_NONE;
}

// INPUT fen, list of moves
extern "C" PyObject* pysfish_legalMoves(PyObject* self, PyObject *args) {
    PyObject* legalMoves = PyList_New(0), *moveList;
    StateListPtr states = StateListPtr(new std::deque<StateInfo>(1));
    Position pos;
    const char *fen;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }
    if(strcmp(fen,"startpos")==0) fen=StartFEN;
    pos.set(fen, Options["UCI_Chess960"], &states->back(), Threads.main());

    // parse move list
    int numMoves = PyList_Size(moveList);
    for (int i=0; i<numMoves ; i++) {
        string moveStr( PyBytes_AS_STRING(PyUnicode_AsEncodedString( PyList_GetItem(moveList, i), "UTF-8", "strict")) );
        Move m;
        if((m = UCI::to_move(pos, moveStr)) != MOVE_NONE)
        {
            // do the move
            states->emplace_back();
            pos.do_move(m, states->back());
        }
        else
        {
            PyErr_SetString(PyExc_ValueError, (string("Invalid move '")+moveStr+"'").c_str());
            return NULL;
        }
    }

    for (const auto& m : MoveList<LEGAL>(pos))
    {
        PyObject *moveStr;
        moveStr=Py_BuildValue("s", UCI::move(m, false).c_str());
        PyList_Append(legalMoves, moveStr);
        Py_XDECREF(moveStr);
    }

    return legalMoves;
}

// Input FEN, list of moves
extern "C" PyObject* pysfish_toSAN(PyObject* self, PyObject *args)
{
    PyObject* sanMoves = PyList_New(0), *moveList;
    StateListPtr states = StateListPtr(new std::deque<StateInfo>(1));
    Position pos;
    const char *fen;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }
    if(strcmp(fen,"startpos")==0) fen=StartFEN;
    pos.set(fen, Options["UCI_Chess960"], &states->back(), Threads.main());

    // parse move list
    int numMoves = PyList_Size(moveList);
    for (int i=0; i<numMoves ; i++) {
        string moveStr( PyBytes_AS_STRING(PyUnicode_AsEncodedString( PyList_GetItem(moveList, i), "UTF-8", "strict")) );
        Move m;
        if((m = UCI::to_move(pos, moveStr)) != MOVE_NONE)
        {
            // add to the san move list
            PyObject *move=Py_BuildValue("s", move_to_san(pos, m).c_str());
            PyList_Append(sanMoves, move);
            Py_XDECREF(move);

            // do the move
            states->emplace_back();
            pos.do_move(m, states->back());
        }
        else
        {
            PyErr_SetString(PyExc_ValueError, (string("Invalid move '")+moveStr+"'").c_str());
            return NULL;
        }
    }
    return sanMoves;
}

// Input FEN, list of moves
extern "C" PyObject* pysfish_getFEN(PyObject* self, PyObject *args) {
    PyObject *moveList;
    StateListPtr states = StateListPtr(new std::deque<StateInfo>(1));
    Position pos;
    const char *fen;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }
    if(strcmp(fen,"startpos")==0) fen=StartFEN;
    pos.set(fen, Options["UCI_Chess960"], &states->back(), Threads.main());

    // parse move list
    int numMoves = PyList_Size(moveList);
    for (int i=0; i<numMoves ; i++) {
        string moveStr( PyBytes_AS_STRING(PyUnicode_AsEncodedString( PyList_GetItem(moveList, i), "UTF-8", "strict")) );
        Move m;
        if((m = UCI::to_move(pos, moveStr)) != MOVE_NONE)
        {
            // do the move
            states->emplace_back();
            pos.do_move(m, states->back());
        }
        else
        {
            PyErr_SetString(PyExc_ValueError, (string("Invalid move '")+moveStr+"'").c_str());
            return NULL;
        }
    }
    return Py_BuildValue("s", pos.fen().c_str());
}

// Input FEN, list of moves
extern "C" PyObject* pysfish_givesCheck(PyObject* self, PyObject *args) {
    PyObject *moveList;
    StateListPtr states = StateListPtr(new std::deque<StateInfo>(1));
    Position pos;
    const char *fen;
    bool givesCheck;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }
    if(strcmp(fen,"startpos")==0) fen=StartFEN;
    pos.set(fen, Options["UCI_Chess960"], &states->back(), Threads.main());

    // parse move list
    int numMoves = PyList_Size(moveList);
    for (int i=0; i<numMoves ; i++) {
        string moveStr( PyBytes_AS_STRING(PyUnicode_AsEncodedString( PyList_GetItem(moveList, i), "UTF-8", "strict")) );
        Move m;
        if((m = UCI::to_move(pos, moveStr)) != MOVE_NONE)
        {
            // do the move
            givesCheck = pos.gives_check(m);
            states->emplace_back();
            pos.do_move(m, states->back());
        }
        else
        {
            PyErr_SetString(PyExc_ValueError, (string("Invalid move '")+moveStr+"'").c_str());
            return NULL;
        }
    }
    return Py_BuildValue("O", givesCheck ? Py_True : Py_False);
}

static PyMethodDef PySFishMethods[] = {
    {"info", (PyCFunction)pysfish_info, METH_NOARGS, "Get Stockfish version info."},
    {"set_option", (PyCFunction)pysfish_setOption, METH_VARARGS, "Set UCI option."},
    {"legal_moves", (PyCFunction)pysfish_legalMoves, METH_VARARGS, "Get legal moves from given FEN and movelist."},
    {"get_fen", (PyCFunction)pysfish_getFEN, METH_VARARGS, "Get resulting FEN from given FEN and movelist."},
    {"to_san", (PyCFunction)pysfish_toSAN, METH_VARARGS, "Converts list of UCI moves to SAN."},
    {"gives_check", (PyCFunction)pysfish_givesCheck, METH_VARARGS, "Get check status from given FEN and movelist."},
    {NULL, NULL, 0, NULL},  // sentinel
};

static PyModuleDef pysfishmodule = {
    PyModuleDef_HEAD_INIT,
    "pysfish",
    "Seirawan-Stockfish extension module.",
    -1,
    PySFishMethods,
};

PyMODINIT_FUNC PyInit_pysfish() {
    PyObject* module;

    module = PyModule_Create(&pysfishmodule);
    if (module == NULL) {
        return NULL;
    }
    PySFishError = PyErr_NewException("pysfish.error", NULL, NULL);
    Py_INCREF(PySFishError);
    PyModule_AddObject(module, "error", PySFishError);

    // initialize stockfish
    UCI::init(Options);
    PSQT::init();
    Bitboards::init();
    Position::init();
    Bitbases::init();
    Search::init();
    Pawns::init();
    Tablebases::init(Options["SyzygyPath"]);
    TT.resize(Options["Hash"]);
    Threads.set(Options["Threads"]);
    Search::clear(); // After threads are up

    return module;
};

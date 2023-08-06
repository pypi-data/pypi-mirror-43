#ifndef SITE_PACKAGE_PATH
#define SITE_PACKAGE_PATH STR_VALUE(SITE_PACKAGE_PATH)
#endif
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
#include "cppjieba/Jieba.hpp"
#include "cppjieba/TextRankExtractor.hpp"
#include <iostream>

using namespace std;
namespace py = pybind11;

const string DICT_PATH = string(SITE_PACKAGE_PATH) + string("cppjieba/dict/jieba.dict.utf8");
const string HMM_PATH = string(SITE_PACKAGE_PATH) + string("cppjieba/dict/hmm_model.utf8");
const string IDF_PATH = string(SITE_PACKAGE_PATH) + string("cppjieba/dict/idf.utf8");
const string STOP_WORD_PATH = string(SITE_PACKAGE_PATH) + string("cppjieba/dict/stop_words.utf8");

using Word = cppjieba::Word;

using WordVector = vector<string>;

using WordsTaged = vector<pair<string, string>>;

struct Tokenizer
{
    cppjieba::Jieba *jieba;

  public:
    Tokenizer()
    {

        jieba = new cppjieba::Jieba(DICT_PATH, HMM_PATH, "", IDF_PATH, STOP_WORD_PATH);
    };

    Tokenizer(const string &main_dict)
    {

        jieba = new cppjieba::Jieba(main_dict, HMM_PATH, "", IDF_PATH, STOP_WORD_PATH);
    };

    Tokenizer(const string &main_dict, const string &user_dict)
    {

        jieba = new cppjieba::Jieba(main_dict, HMM_PATH, user_dict, IDF_PATH, STOP_WORD_PATH);
    };

    Tokenizer(const string &main_dict, const string &user_dict, const string &stop_word_path)
    {
        jieba = new cppjieba::Jieba(main_dict, HMM_PATH, user_dict, IDF_PATH, stop_word_path);
    };

    vector<tuple<string, uint32_t, uint32_t>> tokenize(const string &sentence, const string &mode = "default", bool HMM = true)
    {
        vector<tuple<string, uint32_t, uint32_t>> result;
        vector<Word> words;
        if (mode.compare("default") == 0)
        {
            jieba->Cut(sentence, words, HMM);
        }
        else
        {
            jieba->CutForSearch(sentence, words, HMM);
        }

        vector<Word>::const_iterator it;
        it = words.begin();
        while (it != words.end())
        {
            result.push_back(make_tuple(it->word, it->unicode_offset, it->unicode_offset + it->unicode_length));
            ++it;
        }
        return result;
    };

    void load_userdict(const vector<string> &buf)
    {
        jieba->LoadUserDict(buf);
    };

    void load_userdict(const set<string> &buf)
    {
        jieba->LoadUserDict(buf);
    };

    void load_userdict(const string &path)
    {
        jieba->LoadUserDict(path);
    };

    WordVector cut_internal(const string &sentence, bool cut_all = false, bool HMM = true)
    {
        WordVector words;
        if (!cut_all)
        {
            jieba->Cut(sentence, words, HMM);
        }
        else
        {
            jieba->CutAll(sentence, words);
        }
        return words;
    };

    vector<string> lcut(const string &sentence, bool cut_all = false, bool HMM = true)
    {
        vector<string> words;
        if (!cut_all)
        {
            jieba->Cut(sentence, words, HMM);
        }
        else
        {
            jieba->CutAll(sentence, words);
        }

        return words;
    };

    vector<string> cut_all(const string &sentence)
    {
        vector<string> words;
        jieba->CutAll(sentence, words);
        return words;
    };

    vector<string> lcut_all(const string &sentence)
    {
        vector<string> words;
        jieba->CutAll(sentence, words);
        return words;
    };

    WordVector cut_for_search_internal(const string &sentence, bool HMM = true)
    {
        WordVector words;
        jieba->CutForSearch(sentence, words, HMM);
        return words;
    };

    vector<string> lcut_for_search(const string &sentence, bool HMM = true)
    {
        vector<string> words;
        jieba->CutForSearch(sentence, words, HMM);
        return words;
    };

    WordsTaged tag(const string &sentence)
    {
        WordsTaged words;
        jieba->Tag(sentence, words);
        return words;
    };

    bool add_word(const string &word, const string &tag = cppjieba::UNKNOWN_TAG)
    {
        return jieba->InsertUserWord(word, tag);
    };

    bool add_word(const string &word, int freq, const string &tag = cppjieba::UNKNOWN_TAG)
    {
        return jieba->InsertUserWord(word, freq, tag);
    };

    bool find(const string &word)
    {
        return jieba->Find(word);
    };

    string lookup_tag(const string &word) const
    {
        return jieba->LookupTag(word);
    };
};

namespace Jieba
{
struct KeywordExtractor
{
  private:
    Tokenizer *tokenizer;
    cppjieba::KeywordExtractor *keywordExtractor;

    void initKeyowrdExtractor(const string &idfPath = IDF_PATH,
                              const string &stopWordPath = STOP_WORD_PATH)
    {
        keywordExtractor = new cppjieba::KeywordExtractor(tokenizer->jieba->GetDictTrie(), tokenizer->jieba->GetHMMModel(), idfPath, stopWordPath);
    };

  public:
    KeywordExtractor(Tokenizer *t) : tokenizer(t)
    {
        initKeyowrdExtractor();
    };

    KeywordExtractor(Tokenizer *t, const string &idfPath,
                     const string &stopWordPath) : tokenizer(t)
    {
        initKeyowrdExtractor(idfPath, stopWordPath);
    };

    vector<string> extract_tags(const string &sentence, size_t topK = 20)
    {
        vector<string> keywords;
        keywordExtractor->Extract(sentence, keywords, topK);
        return keywords;
    };
};

struct TextRankExtractor
{
  private:
    Tokenizer *tokenizer;
    cppjieba::TextRankExtractor *textRankExtractor;

    void initTextRankExtractor(const string &stopWordPath = STOP_WORD_PATH)

    {
        textRankExtractor = new cppjieba::TextRankExtractor(tokenizer->jieba->GetDictTrie(), tokenizer->jieba->GetHMMModel(), stopWordPath);
    };

  public:
    TextRankExtractor(Tokenizer *t) : tokenizer(t)
    {
        initTextRankExtractor();
    };

    TextRankExtractor(Tokenizer *t, const string &stopWordPath) : tokenizer(t)
    {
        initTextRankExtractor(stopWordPath);
    };

    vector<string> textrank_no_weight(const string &sentence, size_t topK = 20)
    {
        vector<string> keywords;
        textRankExtractor->Extract(sentence, keywords, topK);
        return keywords;
    };

    vector<pair<string, double>> textrank_with_weight(const string &sentence, size_t topK = 20)
    {
        vector<pair<string, double>> keywords;
        textRankExtractor->Extract(sentence, keywords, topK);
        return keywords;
    };
};

Tokenizer *dt;
KeywordExtractor *keywordExtractor;
TextRankExtractor *textRankExtractor;

void initialize()
{

    dt = new Tokenizer();
};

void init_check()
{
    if (!dt)
    {
        initialize();
    }
};

Tokenizer *get_default_tokenizer()
{
    init_check();
    return dt;
};

void init_check_textrank_extractor()
{
    if (!textRankExtractor)
    {
        textRankExtractor = new TextRankExtractor(get_default_tokenizer());
    }
};

TextRankExtractor *get_default_textrank_extractor()
{
    init_check_textrank_extractor();
    return textRankExtractor;
};

void init_check_keywordExtractor()
{
    if (!keywordExtractor)
    {
        keywordExtractor = new KeywordExtractor(get_default_tokenizer());
    }
};

KeywordExtractor *get_default_keyword_extractor()
{
    init_check_keywordExtractor();
    return keywordExtractor;
};

WordsTaged tag(const string &sentence)
{
    init_check();
    return dt->tag(sentence);
};

WordVector cut(const string &sentence, bool cut_all = false, bool HMM = true)
{
    init_check();
    return dt->cut_internal(sentence, cut_all, HMM);
};

vector<string> lcut(const string &sentence, bool cut_all = false, bool HMM = true)
{
    init_check();
    return dt->lcut(sentence, cut_all, HMM);
};

vector<string> lcut_all(const string &sentence)
{
    init_check();
    return dt->lcut_all(sentence);
};

WordVector cut_for_search(const string &sentence, bool HMM = true)
{
    init_check();
    return dt->cut_for_search_internal(sentence, HMM);
};

vector<string> cut_all(const string &sentence)
{
    init_check();
    return dt->cut_all(sentence);
};

vector<string> lcut_for_search(const string &sentence, bool HMM = true)
{
    init_check();
    return dt->lcut_for_search(sentence, HMM);
};

bool add_word(const string &word, const string &tag = cppjieba::UNKNOWN_TAG)
{
    init_check();
    return dt->add_word(word, tag);
};

bool add_word(const string &word, int freq, const string &tag = cppjieba::UNKNOWN_TAG)
{
    return dt->add_word(word, freq, tag);
};

vector<tuple<string, uint32_t, uint32_t>> tokenize(const string &sentence, const string &mode = "default", bool HMM = true)
{
    init_check();
    return dt->tokenize(sentence, mode, HMM);
};

void load_userdict2(const vector<string> &buf)
{
    init_check();
    dt->load_userdict(buf);
};

void load_userdict3(const set<string> &buf)
{
    init_check();
    dt->load_userdict(buf);
};

void load_userdict(const string &path)
{
    init_check();
    dt->load_userdict(path);
};

bool find(const string &word)
{
    init_check();
    return dt->find(word);
};

const string lookup_tag(const string &word) 
{
    init_check();
    return dt->lookup_tag(word);
};

}; // namespace Jieba

PYBIND11_MODULE(libcppjieba, m)
{
    m.doc() = "python extension for cppjieba"; // optional module docstring

    m.def("cut", &Jieba::cut, py::arg("sentence"), py::arg("cut_all") = false, py::arg("HMM") = true);
    m.def("lcut", &Jieba::lcut, py::arg("sentence"), py::arg("cut_all") = false, py::arg("HMM") = true);
    m.def("cut_all", &Jieba::cut_all);
    m.def("lcut_all", &Jieba::lcut_all);
    m.def("lcut_for_search", &Jieba::lcut_for_search, py::arg("sentence"), py::arg("HMM") = true);
    m.def("cut_for_search", &Jieba::cut_for_search, py::arg("sentence"), py::arg("HMM") = true);
    m.def("tag", &Jieba::tag, py::arg("sentence"));
    m.def("initialize", &Jieba::initialize);
    m.def("get_default_keyword_extractor", &Jieba::get_default_keyword_extractor);
    m.def("get_default_textrank_extractor", &Jieba::get_default_textrank_extractor);
    m.def("add_word", (bool (*)(const string &, const string &)) & Jieba::add_word, py::arg("word"), py::arg("tag") = cppjieba::UNKNOWN_TAG);
    m.def("add_word", (bool (*)(const string &, int freq, const string & )) & Jieba::add_word, py::arg("word"), py::arg("freq"), py::arg("tag") = cppjieba::UNKNOWN_TAG);
    m.def("tokenize", &Jieba::tokenize, py::arg("sentence"), py::arg("mode") = "default", py::arg("HMM") = true);
    m.def("load_userdict", (void (*)(const vector<string> &)) & Jieba::load_userdict2);
    m.def("load_userdict", (void (*)(const set<string> &)) & Jieba::load_userdict3);
    m.def("load_userdict", (void (*)(const string &)) & Jieba::load_userdict);
    m.def("find", &Jieba::find);
    m.def("lookup_tag", &Jieba::lookup_tag);

    py::class_<Jieba::KeywordExtractor>(m, "KeywordExtractor")
        .def(py::init<Tokenizer *>())
        .def(py::init<Tokenizer *, const string &, const string &>())
        .def("extract_tags", &Jieba::KeywordExtractor::extract_tags, py::arg("sentence"), py::arg("topK") = 20);

    py::class_<Jieba::TextRankExtractor>(m, "TextRankExtractor")
        .def(py::init<Tokenizer *>())
        .def(py::init<Tokenizer *, const string &>())
        .def("textrank_no_weight", &Jieba::TextRankExtractor::textrank_no_weight, py::arg("sentence"), py::arg("topK") = 20)
        .def("textrank_with_weight", &Jieba::TextRankExtractor::textrank_with_weight, py::arg("sentence"), py::arg("topK") = 20);

    py::class_<Tokenizer>(m, "Tokenizer")
        .def(py::init<>())
        .def(py::init<const string &>())
        .def(py::init<const string &, const string &>())
        .def(py::init<const string &, const string &, const string &>())
        .def("cut_internal", &Tokenizer::cut_internal, py::arg("sentence"), py::arg("cut_all") = false, py::arg("HMM") = true)
        .def("lcut", &Tokenizer::lcut, py::arg("sentence"), py::arg("cut_all") = false, py::arg("HMM") = true)
        .def("lcut_all", &Tokenizer::lcut_all)
        .def("cut_all", &Tokenizer::cut_all)
        .def("lcut_for_search", &Tokenizer::lcut_for_search, py::arg("sentence"), py::arg("HMM") = true)
        .def("cut_for_search_internal", &Tokenizer::cut_for_search_internal, py::arg("sentence"), py::arg("HMM") = true)
        .def("tag", &Tokenizer::tag, py::arg("sentence"))
        .def("add_word", (bool (Tokenizer::*)(const string &, const string & )) & Tokenizer::add_word, py::arg("word"), py::arg("tag") = cppjieba::UNKNOWN_TAG)
        .def("add_word", (bool (Tokenizer::*)(const string &, int freq, const string & )) & Tokenizer::add_word, py::arg("word"), py::arg("freq"), py::arg("tag") = cppjieba::UNKNOWN_TAG)
        .def("tokenize", &Tokenizer::tokenize, py::arg("sentence"), py::arg("mode") = "default", py::arg("HMM") = true)
        .def("load_userdict", (void (Tokenizer::*)(const vector<string> &)) & Tokenizer::load_userdict)
        .def("load_userdict", (void (Tokenizer::*)(const string &)) & Tokenizer::load_userdict)
        .def("load_userdict", (void (Tokenizer::*)(const set<string> &)) & Tokenizer::load_userdict)
        .def("find", &Tokenizer::find)
        .def("lookup_tag", &Tokenizer::lookup_tag);
    // py::class_<Word>(m, "Word")
    //     .def_readonly("word", &Word::word)
    //     .def("__str__", [](const Word &v) {
    //         return v.word;
    //     })
    //     .def("__repr__", [](const Word &v) {
    //         return v.word;
    //     });
}
// Chemfiles, a modern library for chemistry file reading and writing
// Copyright (C) Guillaume Fraux and contributors -- BSD license

#include <algorithm>

#include "chemfiles/files/PlainFile.hpp"
#include "chemfiles/files/GzFile.hpp"
#include "chemfiles/files/XzFile.hpp"
#include "chemfiles/ErrorFmt.hpp"
#include "chemfiles/unreachable.hpp"
using namespace chemfiles;

std::unique_ptr<TextFile> TextFile::open(std::string path, File::Mode mode, File::Compression compression) {
    switch (compression) {
    case File::DEFAULT:
        return std::unique_ptr<TextFile>(new PlainFile(std::move(path), mode));
    case File::GZIP:
        return std::unique_ptr<TextFile>(new GzFile(std::move(path), mode));
    case File::LZMA:
        return std::unique_ptr<TextFile>(new XzFile(std::move(path), mode));
    }
    unreachable();
}

TextFile::TextFile(std::string path, File::Mode mode, File::Compression compression, std::streambuf* buffer):
    File(std::move(path), mode, compression), std::iostream(buffer)
{
    std::iostream::clear();
    // Throw exceptions on errors
    std::iostream::exceptions(std::fstream::badbit | std::fstream::failbit);
}

/// Read a single line from `stream` in `string`, handling all possible end of
/// line markers (`\n`, `\r`, `\r\n`).
///
/// Code from http://stackoverflow.com/a/6089413
void TextFile::get_line(std::string& string) {
    string.clear();

    // The characters in the stream are read one-by-one using a std::streambuf.
    // That is faster than reading them one-by-one using the std::istream.
    // Code that uses streambuf this way must be guarded by a sentry object.
    // The sentry object performs various tasks,
    // such as thread synchronization and updating the stream state.
    std::istream::sentry sentry(*this, true);
    std::streambuf* buffer = std::istream::rdbuf();

    while(true) {
        int c = buffer->sbumpc();
        switch (c) {
        case '\n':
            return;
        case '\r':
            if(buffer->sgetc() == '\n') {
                buffer->sbumpc();
            }
            return;
        case EOF:
            // Also handle the case when the last line has no line ending
            if(string.empty()) {
                std::istream::setstate(std::ios::eofbit);
            }
            return;
        default:
            string.push_back(static_cast<char>(c));
        }
    }
}

void TextFile::rewind() {
    std::istream::clear();
    std::istream::seekg(0, std::ios::beg);
}

bool TextFile::eof() {
    return std::istream::eof();
}

std::string TextFile::readline() {
    // Disable exceptions checking, and manually check bellow
    auto state = this->exceptions();
    this->exceptions(std::fstream::goodbit);
    std::string line;
    get_line(line);
    if (this->fail()) {
        throw file_error("could not read a line in {}", this->path());
    }
    // Re-enable exceptions checking
    this->exceptions(state);
    return line;
}

std::vector<std::string> TextFile::readlines(size_t n) {
    // Disable exceptions checking, and manually check bellow
    auto state = this->exceptions();
    this->exceptions(std::fstream::goodbit);

    auto lines = std::vector<std::string>(n);
    for (size_t i = 0; i < n; i++) {
        get_line(lines[i]);
    }

    if (this->fail()) {
        throw file_error("could not read a line in {}", this->path());
    }
    // Re-enable exceptions checking
    this->exceptions(state);
    return lines;
}

// Chemfiles, a modern library for chemistry file reading and writing
// Copyright (C) Guillaume Fraux and contributors -- BSD license

#include <cassert>
#include <sstream>

#include <fmt/format.h>
#include <fmt/ostream.h>

#include "chemfiles/formats/XYZ.hpp"

#include "chemfiles/ErrorFmt.hpp"
#include "chemfiles/File.hpp"
#include "chemfiles/Frame.hpp"
#include "chemfiles/utils.hpp"

using namespace chemfiles;

template<> FormatInfo chemfiles::format_information<XYZFormat>() {
    return FormatInfo("XYZ").with_extension(".xyz").description(
        "XYZ text format"
    );
}

/// Fast-forward the file for one step, returning `false` if the file does
/// not contain one more step.
static bool forward(TextFile& file);

XYZFormat::XYZFormat(std::string path, File::Mode mode, File::Compression compression)
    : file_(TextFile::open(std::move(path), mode, compression))
{
    while (!file_->eof()) {
        auto position = file_->tellg();
        if (!file_ || position == std::streampos(-1)) {
            throw format_error("IO error while reading '{}' as XYZ", path);
        }
        if (forward(*file_)) {
            steps_positions_.push_back(position);
        }
    }
    file_->rewind();
}

size_t XYZFormat::nsteps() {
    return steps_positions_.size();
}

void XYZFormat::read_step(const size_t step, Frame& frame) {
    assert(step < steps_positions_.size());
    file_->seekg(steps_positions_[step]);
    read(frame);
}

void XYZFormat::read(Frame& frame) {
    size_t natoms = 0;
    try {
        natoms = parse<size_t>(file_->readline());
        file_->readline(); // XYZ comment line;
    } catch (const std::exception& e) {
        throw format_error("can not read next step as XYZ: {}", e.what());
    }

    frame.reserve(natoms);
    frame.resize(0);

    for (const auto& line: file_->readlines(natoms)) {
        double x = 0, y = 0, z = 0;
        char name[32] = {0};
        scan(line, "%31s %lf %lf %lf", &name[0], &x, &y, &z);
        frame.add_atom(Atom(name), Vector3D(x, y, z));
    }
}

void XYZFormat::write(const Frame& frame) {
    auto& topology = frame.topology();
    auto& positions = frame.positions();
    assert(frame.size() == topology.size());

    fmt::print(*file_, "{}\n", frame.size());
    fmt::print(*file_, "Written by the chemfiles library\n", frame.size());

    for (size_t i = 0; i < frame.size(); i++) {
        auto name = topology[i].name();
        if (name == "") {name = "X";}
        fmt::print(
            *file_, "{} {} {} {}\n",
            name, positions[i][0], positions[i][1], positions[i][2]
        );
    }

    steps_positions_.push_back(file_->tellg());
}

bool forward(TextFile& file) {
    if (!file) {return false;}

    size_t natoms = 0;
    try {
        natoms = parse<size_t>(file.readline());
    } catch (const FileError&) {
        // No more line left in the file
        return false;
    } catch (const Error&) {
        // We could not read an integer, so give up here
        return false;
    }

    try {
        file.readlines(natoms + 1);
    } catch (const FileError& e) {
        // We could not read the lines from the file
        throw format_error(
            "not enough lines for XYZ format: {}", file.path(), e.what()
        );
    }
    return true;
}

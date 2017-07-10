exists($$[QT_INSTALL_BINS]/qdoc):exists($$[QT_INSTALL_BINS]/qhelpgenerator) {
    check_qdoc = "qdoc/qhelpgenerator in $$[QT_INSTALL_BINS]"
    QDOC = $$[QT_INSTALL_BINS]/qdoc
    QHELPGENERATOR = $$[QT_INSTALL_BINS]/qhelpgenerator
} else {
    check_qdoc = "qdoc/qhelpgenerator in PATH"
    QDOC = qdoc
    QHELPGENERATOR = qhelpgenerator
}

defineReplace(cmdEnv) {
    !equals(QMAKE_DIR_SEP, /): 1 ~= s,^(.*)$,(set \\1) &&,g
    return("$$1")
}

defineReplace(qdoc) {
    return("$$cmdEnv(OUTDIR=$$1 QMLLIVE_VERSION=$$VERSION QMLLIVE_VERSION_TAG=$$VERSION_TAG QT_INSTALL_DOCS=$$[QT_INSTALL_DOCS/src]) $$QDOC")
}

html-docs.commands = $$qdoc($$BUILD_DIR/doc/html) $$PWD/plugin.qdocconf
html-docs.files = $$BUILD_DIR/doc/html

docs.depends = html-docs

QMAKE_EXTRA_TARGETS += html-docs docs


OTHER_FILES += \
    $$PWD/*.qdocconf \
    $$PWD/*.qdoc \
    $$PWD/examples/*.qdoc \
    $$PWD/images/*.png

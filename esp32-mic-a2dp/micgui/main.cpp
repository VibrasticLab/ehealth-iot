#include "guimic.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    guimic w;
    w.show();
    return a.exec();
}

#include "cough.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Cough w;
    w.show();
    return a.exec();
}

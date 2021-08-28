#ifndef COUGH_H
#define COUGH_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class Cough; }
QT_END_NAMESPACE

class Cough : public QMainWindow
{
    Q_OBJECT

public:
    Cough(QWidget *parent = nullptr);
    ~Cough();

private:
    Ui::Cough *ui;
};
#endif // COUGH_H

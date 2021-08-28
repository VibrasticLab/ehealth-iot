#ifndef COUGH_H
#define COUGH_H

#include <QMainWindow>
#include <QTimer>
#include <QRandomGenerator>
#include <qwt_plot_curve.h>
#include <cmath>

QT_BEGIN_NAMESPACE
namespace Ui { class Cough; }
QT_END_NAMESPACE

class Cough : public QMainWindow
{
    Q_OBJECT

public:
    Cough(QWidget *parent = nullptr);
    ~Cough();

    QTimer *tmrUpdate;

public slots:
    void dataUpdate();

private:
    Ui::Cough *ui;

    QwtPlotCurve *curve;
    static const uint8_t plotDataSize = 100;

    double xData[plotDataSize];
    double yData[plotDataSize];
};
#endif // COUGH_H

#ifndef GUIMIC_H
#define GUIMIC_H

#include <qwt/qwt_plot_curve.h>
#include <QSerialPort>
#include <QMainWindow>
#include <QMessageBox>

QT_BEGIN_NAMESPACE
namespace Ui { class guimic; }
QT_END_NAMESPACE

class guimic : public QMainWindow
{
    Q_OBJECT

public:
    guimic(QWidget *parent = nullptr);
    ~guimic();

private slots:
    void on_btnOpen_clicked();

private:
    Ui::guimic *ui;
    QSerialPort *port;
    QwtPlotCurve *curve;

    static const int plotDataSize = 100;

    double xData[plotDataSize];
    double yData[plotDataSize];
};
#endif // GUIMIC_H

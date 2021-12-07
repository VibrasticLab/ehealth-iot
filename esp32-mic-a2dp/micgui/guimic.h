#ifndef GUIMIC_H
#define GUIMIC_H

#include <qwt/qwt_plot_curve.h>
#include <QSerialPort>
#include <QMainWindow>
#include <QMessageBox>
#include <QTimer>

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
    void on_btnStart_clicked();

    void req_data();
    void get_data();
    int check_data(QString strInput);
    void parse_data(QString strInput);

private:
    Ui::guimic *ui;
    QSerialPort *port;
    QwtPlotCurve *curve;
    QTimer* tmr;

    QByteArray rawdata;
    bool dataproc = false;

    static const int plotDataSize = 252;
    uint16_t vnum;

    double xData[plotDataSize];
    double yData[plotDataSize];
};
#endif // GUIMIC_H

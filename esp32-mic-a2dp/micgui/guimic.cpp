#include "guimic.h"
#include "ui_guimic.h"

#include <cmath>

guimic::guimic(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::guimic)
{
    ui->setupUi(this);

    port = new QSerialPort(this);

    for(int idx=0;idx<plotDataSize;++idx){
        xData[idx] = idx;
        yData[idx] = sin(M_PI * idx/50);
    }

    curve = new QwtPlotCurve;
    curve->setSamples(xData,yData,plotDataSize);
    curve->attach(ui->plot);

    ui->plot->replot();
    ui->plot->show();
}

guimic::~guimic()
{
    delete ui;
}

void guimic::on_btnOpen_clicked()
{
    QString dev_name="/dev/ttyUSB0";
    QSerialPort::BaudRate dev_baud=QSerialPort::Baud115200;

    if(ui->btnOpen->text()=="Open"){
        port->setPortName(dev_name);
        if(port->open(QIODevice::ReadWrite)){
            port->setBaudRate(dev_baud,QSerialPort::AllDirections);
            port->setDataBits(QSerialPort::Data8);
            port->setStopBits(QSerialPort::OneStop);
            port->setFlowControl(QSerialPort::NoFlowControl);
            port->setParity(QSerialPort::NoParity);

            QMessageBox::information(this,"SUCCESS","port opened "+ dev_name);
            ui->btnOpen->setText("Close");
        }
        else{
            QMessageBox::critical(this,"FAILED","port failed " + dev_name);
            ui->btnOpen->setText("Open");
        }
    }
    else{
        if(port->isOpen()) port->close();
        ui->btnOpen->setText("Open");
    }
}


#include "guimic.h"
#include "ui_guimic.h"

guimic::guimic(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::guimic)
{
    ui->setupUi(this);

    port = new QSerialPort(this);
    connect(port,SIGNAL(readyRead()),SLOT(get_data()));

    tmr = new QTimer(this);
    connect(tmr,SIGNAL(timeout()),SLOT(req_data()));

    for(int idx=0;idx<plotDataSize;++idx){
        xData[idx] = idx;
        yData[idx] = 0;
    }

    ui->plot->setAxisScale(0,0,256);

    curve = new QwtPlotCurve;
    curve->setRawSamples(xData,yData,plotDataSize);
    curve->attach(ui->plot);

    ui->plot->replot();

    ui->numv->setText(QString::number(0));
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

void guimic::on_btnStart_clicked()
{
    ui->rxbuff->clear();

    if(!port->isOpen()) return;

    if(ui->btnStart->text()=="Start"){
        tmr->start(500);
        ui->btnStart->setText("Stop");
    }
    else{
        tmr->stop();
        ui->btnStart->setText("Start");
    }
}

void guimic::req_data(){
    if(!port->isOpen())return;

    if(!dataproc){
        ui->rxbuff->clear();
        QByteArray datareq = "get\r\n";
        port->write(datareq);
    }
}

void guimic::get_data(){
    rawdata = port->readLine();

    if(rawdata.size()>10) ui->rxbuff->insertPlainText(rawdata);

    if(ui->rxbuff->toPlainText().isEmpty())return;
    vnum = check_data(ui->rxbuff->toPlainText());

    if(vnum>245){
        dataproc = true;
        ui->numv->setText(QString::number(vnum));
        parse_data(ui->rxbuff->toPlainText());
    }
}

int guimic::check_data(QString strInput){
    QStringList strVal = strInput.split(",");
    return strVal.count();
}

void guimic::parse_data(QString strInput){
    QStringList strVal = strInput.split(",");
    uint16_t idx;

    for(idx=0;idx<plotDataSize;idx++){
        yData[idx] = 0;
    }

    for(idx=0;idx<vnum;idx++){
        yData[idx] = strVal[idx].toInt() / 500;
    }

    curve->setRawSamples(xData,yData,plotDataSize);
    curve->attach(ui->plot);

    ui->plot->replot();

    dataproc = false;
}

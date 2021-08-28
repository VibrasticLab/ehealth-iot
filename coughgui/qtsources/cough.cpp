#include "cough.h"
#include "ui_cough.h"

Cough::Cough(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Cough)
{
    this->setFixedSize(QSize(480, 320));
    ui->setupUi(this);

    for(uint8_t idx=0;idx<plotDataSize;++idx){
        xData[idx] = idx;
        yData[idx] = sin(M_PI*idx/50);
    }

    QPen crvpen = QPen(Qt::red, 4.0);
    crvpen.setCosmetic(false);

    curve = new QwtPlotCurve();
    curve->setPen(crvpen);
    curve->setRawSamples(xData,yData,plotDataSize);
    curve->attach(ui->plotMain);

    ui->plotMain->replot();
    ui->plotMain->show();

    tmrUpdate = new QTimer(this);
    connect(tmrUpdate,SIGNAL(timeout()),this,SLOT(dataUpdate()));
    tmrUpdate->start(100);
}

Cough::~Cough()
{
    delete ui;
}

void Cough::dataUpdate(){
    uint8_t rndfreq;

    rndfreq = QRandomGenerator::global()->bounded(0,10);
    for(uint8_t idx=0;idx<plotDataSize;++idx){
        yData[idx] = sin(rndfreq*M_PI*idx/50);
    }
    curve->setRawSamples(xData,yData,plotDataSize);
    ui->plotMain->replot();
}


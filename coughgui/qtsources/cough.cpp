#include "cough.h"
#include "ui_cough.h"

Cough::Cough(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Cough)
{
    this->setFixedSize(QSize(480, 320));
    ui->setupUi(this);
}

Cough::~Cough()
{
    delete ui;
}


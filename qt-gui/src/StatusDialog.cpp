#include "StatusDialog.h"
#include <QVBoxLayout>
#include <QHeaderView>


StatusDialog::StatusDialog(VpnBackend *backend, const QString &account, QWidget *parent)
    : QDialog(parent), vpnBackend(backend), accountName(account) {
    setupUi();
    refreshTimer = new QTimer(this);
    connect(refreshTimer, &QTimer::timeout, this, &StatusDialog::refreshStatus);
    refreshTimer->start(2000); // Refresh every 2 seconds
    refreshStatus();
}


void StatusDialog::setupUi() {
    setWindowTitle("Connection Status");
    resize(600, 400);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    summaryLabel = new QLabel("Status summary will appear here.", this);
    statusTable = new QTableWidget(this);
    statusTable->setColumnCount(2);
    statusTable->setHorizontalHeaderLabels({"Property", "Value"});
    statusTable->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    statusTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    buttonBox = new QDialogButtonBox(QDialogButtonBox::Ok, this);
    mainLayout->addWidget(summaryLabel);
    mainLayout->addWidget(statusTable);
    mainLayout->addWidget(buttonBox);
    connect(buttonBox, &QDialogButtonBox::accepted, this, &QDialog::accept);
}

void StatusDialog::refreshStatus() {
    if (!vpnBackend) return;
    QVariantMap status = vpnBackend->getStatus(accountName);
    setStatusData(status);
}

void StatusDialog::setStatusData(const QVariantMap &status) {
    summaryLabel->setText(status.value("Summary").toString());
    statusTable->setRowCount(status.size() - 1);
    int row = 0;
    for (auto it = status.begin(); it != status.end(); ++it) {
        if (it.key() == "Summary") continue;
        statusTable->setItem(row, 0, new QTableWidgetItem(it.key()));
        statusTable->setItem(row, 1, new QTableWidgetItem(it.value().toString()));
        ++row;
    }
}

QVariantMap StatusDialog::statusData() const {
    QVariantMap status;
    status["Summary"] = summaryLabel->text();
    for (int i = 0; i < statusTable->rowCount(); ++i) {
        QString key = statusTable->item(i, 0)->text();
        QString value = statusTable->item(i, 1)->text();
        status[key] = value;
    }
    return status;
}

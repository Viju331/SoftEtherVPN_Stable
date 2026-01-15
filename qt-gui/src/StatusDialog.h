#pragma once
#include <QDialog>
#include <QLabel>
#include <QTableWidget>
#include <QDialogButtonBox>


#include <QTimer>
#include "VpnBackend.h"

class StatusDialog : public QDialog {
    Q_OBJECT
public:
    StatusDialog(VpnBackend *backend, const QString &accountName, QWidget *parent = nullptr);
    void setStatusData(const QVariantMap &status);
    QVariantMap statusData() const;
private slots:
    void refreshStatus();
private:
    QLabel *summaryLabel;
    QTableWidget *statusTable;
    QDialogButtonBox *buttonBox;
    QTimer *refreshTimer;
    VpnBackend *vpnBackend;
    QString accountName;
    void setupUi();
};

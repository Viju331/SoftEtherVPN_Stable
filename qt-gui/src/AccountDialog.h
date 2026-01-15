#pragma once
#include <QDialog>
#include <QLineEdit>
#include <QComboBox>
#include <QCheckBox>
#include <QTabWidget>
#include <QDialogButtonBox>

class AccountDialog : public QDialog {
    Q_OBJECT
public:
    AccountDialog(QWidget *parent = nullptr);
    void setAccountData(const QVariantMap &data);
    QVariantMap accountData() const;
private:
    QTabWidget *tabWidget;
    // General tab
    QLineEdit *nameEdit, *serverEdit, *portEdit, *hubEdit;
    QComboBox *adapterCombo;
    QCheckBox *startupCheck;
    // Auth tab
    QComboBox *authTypeCombo;
    QLineEdit *usernameEdit, *passwordEdit;
    // Advanced tab
    QLineEdit *tcpConnEdit, *timeoutEdit;
    QCheckBox *halfConnCheck, *udpAccelCheck, *compressCheck, *bridgeCheck, *monitorCheck;
    QComboBox *cipherCombo;
    // Proxy tab
    QComboBox *proxyTypeCombo;
    QLineEdit *proxyHostEdit, *proxyPortEdit, *proxyUserEdit, *proxyPassEdit;
    QDialogButtonBox *buttonBox;
    void setupUi();
};

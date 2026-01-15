#pragma once
#include <QObject>
#include <QVariantMap>
#include <QVariantList>

class VpnBackend : public QObject {
    Q_OBJECT
public:
    explicit VpnBackend(QObject *parent = nullptr);
    // Account management
    bool addAccount(const QVariantMap &account);
    bool editAccount(const QVariantMap &account);
    bool deleteAccount(const QString &accountName);
    QVariantList listAccounts() const;
    // VLAN management
    bool setVLANs(const QVariantList &vlans);
    QVariantList getVLANs() const;
    // Status
    QVariantMap getStatus(const QString &accountName) const;
    // Initialization
    bool initialize();
};

#include "MainWindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName("SoftEther VPN Server");
    MainWindow w;
    w.setWindowTitle("SoftEther VPN Server");
    w.show();
    return app.exec();
}

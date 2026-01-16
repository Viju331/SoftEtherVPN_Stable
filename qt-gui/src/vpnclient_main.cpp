#include "MainWindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    app.setApplicationName("SoftEther VPN Client");
    MainWindow w;
    w.setWindowTitle("SoftEther VPN Client");
    w.show();
    return app.exec();
}

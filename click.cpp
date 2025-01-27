#include <iostream>
#include <windows.h>
#include <string>
#include <thread>
#include <chrono>

void clickMouse(const std::string& clickType) {
    if (clickType == "left") {
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }
    else if (clickType == "mid") {
        mouse_event(MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0);
    }
    else if (clickType == "right") {
        mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <hotkey> <interval> <click_type>" << std::endl;
        return 1;
    }

    // 获取命令行参数
    std::string hotkey_str = argv[1];
    int hotkey = std::stoi(hotkey_str);
    double interval = std::stod(argv[2]);
    std::string clickType = argv[3];

    // 隐藏控制台窗口
    HWND consoleWindow = GetConsoleWindow();
    ShowWindow(consoleWindow, SW_HIDE);

    bool click = false;
    bool keyPreviouslyPressed = false;  // 记录按键是否已被按下
    auto next_click_time = std::chrono::steady_clock::now();

    while (true) {
        SHORT keyState = GetAsyncKeyState(hotkey);
        bool isKeyPressed = (keyState & 0x8000) != 0;  // 检测按键是否处于按下状态

        if (isKeyPressed && !keyPreviouslyPressed) {
            // 仅当按键从未按下（松开）切换为按下时触发
            click = !click;
            Sleep(100);
        }

        keyPreviouslyPressed = isKeyPressed;  // 更新按键状态

        if (click) {
            auto now = std::chrono::steady_clock::now();
            if (now >= next_click_time) {
                std::thread clickThread(clickMouse, clickType);
                clickThread.detach();
                next_click_time = now + std::chrono::milliseconds(static_cast<int>(interval * 1000));
            }
        }

        Sleep(1);  // 减少 CPU 占用
    }

    return 0;
}

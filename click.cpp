#include <Windows.h>
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <random> // 添加头文件
#pragma pack(push, 1)
struct SharedParams {
    int version;        // 版本号校验
    int hotkey;
    double interval;
    int clickType;
};
#pragma pack(pop)
// 控制标识
const int APP_VERSION = 0x2023ABCD;  // 唯一版本标识
const int MIN_HOTKEY = 1;
const int MAX_HOTKEY = 254;


void clickMouse(int clickType) {
    INPUT inputs[2] = {};
    ZeroMemory(inputs, sizeof(inputs));

    switch (clickType) {
    case 0: // 左键
        inputs[0].type = INPUT_MOUSE;
        inputs[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
        inputs[1].type = INPUT_MOUSE;
        inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTUP;
        break;
    case 1: // 中键
        inputs[0].type = INPUT_MOUSE;
        inputs[0].mi.dwFlags = MOUSEEVENTF_MIDDLEDOWN;
        inputs[1].type = INPUT_MOUSE;
        inputs[1].mi.dwFlags = MOUSEEVENTF_MIDDLEUP;
        break;
    case 2: // 右键
        inputs[0].type = INPUT_MOUSE;
        inputs[0].mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
        inputs[1].type = INPUT_MOUSE;
        inputs[1].mi.dwFlags = MOUSEEVENTF_RIGHTUP;
        break;
    }

    SendInput(2, inputs, sizeof(INPUT));
}

bool validate_parameters(const SharedParams& params) {
    return params.version == APP_VERSION &&
        params.hotkey >= MIN_HOTKEY &&
        params.hotkey <= MAX_HOTKEY &&
        params.interval > 0 &&
        params.interval < 3600.0 &&
        params.clickType >= 0 &&
        params.clickType <= 2;
}

int main(int argc, char* argv[]) {
    // 验证启动方式
    if (argc != 2 || std::stoi(argv[1]) != APP_VERSION) {
        MessageBoxW(nullptr, L"请通过主程序启动本工具", L"启动方式错误", MB_ICONERROR | MB_OK);
        return 1;
    }
    // 共享内存访问
    const wchar_t* shmName = L"Local\\ClickParamsSharedMemory";
    HANDLE hMapFile = OpenFileMappingW(FILE_MAP_READ, FALSE, shmName);
    if (!hMapFile) {
        MessageBoxW(NULL, L"未获取到有效参数\n请重新启动功能", L"参数错误", MB_ICONERROR | MB_OK);
        return 2;
    }
    SharedParams* pParams = (SharedParams*)MapViewOfFile(hMapFile, FILE_MAP_READ, 0, 0, sizeof(SharedParams));
    if (!pParams || !validate_parameters(*pParams)) {
        MessageBoxW(NULL, L"参数校验失败\n请检查主程序状态", L"参数错误", MB_ICONERROR | MB_OK);
        if (hMapFile) CloseHandle(hMapFile);
        return 3;
    }


    // 读取参数
    int hotkey = pParams->hotkey;
    double interval = pParams->interval;
    int clickType = pParams->clickType;

    // 初始化随机数生成器
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.9, 1.1);

    // 隐藏控制台窗口
    HWND consoleWindow = GetConsoleWindow();
    ShowWindow(consoleWindow, SW_HIDE);

    bool click = false;
    bool keyPreviouslyPressed = false;
    auto next_click_time = std::chrono::steady_clock::now();

    while (true) {
        // 每次循环都重新读取内存数据
        SharedParams currentParams;
        memcpy(&currentParams, pParams, sizeof(SharedParams));

        // 使用新参数
        int hotkey = currentParams.hotkey;
        double interval = currentParams.interval;
        int clickType = currentParams.clickType;
        SHORT keyState = GetAsyncKeyState(hotkey);
        bool isKeyPressed = (keyState & 0x8000) != 0;
        // 参数有效性检查
        if (!validate_parameters(currentParams)) {
            MessageBoxW(NULL, L"运行时参数失效\n即将退出", L"参数错误", MB_ICONERROR | MB_OK);
            break;
        }

        if (isKeyPressed && !keyPreviouslyPressed) {
            click = !click;
            Sleep(100);
        }

        keyPreviouslyPressed = isKeyPressed;

        if (click) {
            auto now = std::chrono::steady_clock::now();
            if (now >= next_click_time) {
                std::thread clickThread(clickMouse, clickType);
                clickThread.detach();
                //next_click_time = now + std::chrono::milliseconds(static_cast<int>(interval * 1000));
                // 生成随机间隔
                double random_factor = dis(gen);
                double current_interval = interval * random_factor;
                next_click_time = now + std::chrono::milliseconds(
                    static_cast<int>(current_interval * 1000)
                );
            }
        }

        Sleep(1);
    }

    // 清理（理论上不会执行到这里）
    UnmapViewOfFile(pParams);
    CloseHandle(hMapFile);
    return 0;
}

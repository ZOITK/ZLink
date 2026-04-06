using System;

namespace Zoit.Logger
{
    public static class ClientLogger
    {
        public enum LogLevel { Debug = 0, Info = 1, Warn = 2, Error = 3 }
        public static LogLevel CurrentLevel = LogLevel.Info;

        public static void Debug(string msg) => Log(LogLevel.Debug, msg);
        public static void Info(string msg) => Log(LogLevel.Info, msg);
        public static void Warn(string msg) => Log(LogLevel.Warn, msg);
        public static void Error(string msg) => Log(LogLevel.Error, msg);
        public static void Error(string msg, Exception ex) => Log(LogLevel.Error, $"{msg} - {ex.Message}\n{ex.StackTrace}");

        private static void Log(LogLevel level, string message)
        {
            if (level < CurrentLevel) return;

            string timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff");
            string formatted = $"[{timestamp}] [{level.ToString().ToUpper()}] {message}";

#if UNITY_2017_1_OR_NEWER
            if (level == LogLevel.Error) UnityEngine.Debug.LogError(formatted);
            else if (level == LogLevel.Warn) UnityEngine.Debug.LogWarning(formatted);
            else UnityEngine.Debug.Log(formatted);
#else
            Console.WriteLine(formatted);
#endif
        }
    }
}

using System;
using UnityEngine;

namespace Zlink
{
    /// <summary>
    /// C# 클라이언트 로거 (Unity/Console 지원)
    /// </summary>
    public static class Logger
    {
        private const string Prefix = "[zLink] ";

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Info(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            UnityEngine.Debug.Log(Prefix + Message);
#else
            Console.WriteLine(Prefix + Message);
#endif
        }

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Debug(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            UnityEngine.Debug.Log(Prefix + Message);
#else
            System.Diagnostics.Debug.WriteLine(Prefix + Message);
#endif
        }

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Warn(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            UnityEngine.Debug.LogWarning(Prefix + Message);
#else
            Console.WriteLine(Prefix + "[WARN] " + Message);
#endif
        }

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Error(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            UnityEngine.Debug.LogError(Prefix + Message);
#else
            Console.Error.WriteLine(Prefix + Message);
#endif
        }
    }
}

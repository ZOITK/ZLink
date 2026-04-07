using System;
using UnityEngine;

namespace Zoit.Logger
{
    /// <summary>
    /// C# 클라이언트 로거 (Unity/Console 지원)
    /// </summary>
    public static class ClientLogger
    {
        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Info(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            Debug.Log(Message);
#else
            Console.WriteLine(Message);
#endif
        }

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Debug(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            UnityEngine.Debug.Log(Message);
#else
            System.Diagnostics.Debug.WriteLine(Message);
#endif
        }

        [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        public static void Error(string Message)
        {
#if UNITY_2017_1_OR_NEWER
            UnityEngine.Debug.LogError(Message);
#else
            Console.Error.WriteLine(Message);
#endif
        }
    }
}

// Package logger - 범용 로거 라이브러리 (Python 형식 통일)
package logger

import (
	"context"
	"fmt"
	"io"
	"log/slog"
	"os"
	"strings"
)

// CustomTextHandler - Python과 동일한 형식 [YYYY-MM-DD HH:MM:SS] [LEVEL] [zLink] 메시지
type CustomTextHandler struct {
	w io.Writer
}

// NewCustomTextHandler - 커스텀 핸들러 생성
func NewCustomTextHandler(w io.Writer) *CustomTextHandler {
	return &CustomTextHandler{w: w}
}

// Handle - 로그 처리
func (h *CustomTextHandler) Handle(ctx context.Context, r slog.Record) error {
	// 시간 포맷: [YYYY-MM-DD HH:MM:SS]
	timeStr := r.Time.Format("2006-01-02 15:04:05")

	// 레벨: [INFO], [WARN], [ERROR], [DEBUG]
	levelStr := strings.ToUpper(r.Level.String())

	// 메시지와 속성 조합
	msg := r.Message
	attrs := ""
	r.Attrs(func(a slog.Attr) bool {
		attrs += fmt.Sprintf(" %s=%v", a.Key, a.Value.String())
		return true
	})

	// 최종 포맷: [YYYY-MM-DD HH:MM:SS] [LEVEL] [zLink] 메시지 attr1=val1 attr2=val2
	output := fmt.Sprintf("[%s] [%s] [zLink] %s%s\n", timeStr, levelStr, msg, attrs)
	h.w.Write([]byte(output))
	return nil
}

// WithAttrs - 속성 추가
func (h *CustomTextHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return h
}

// WithGroup - 그룹 추가
func (h *CustomTextHandler) WithGroup(name string) slog.Handler {
	return h
}

// Enabled - 로그 레벨 활성화 확인
func (h *CustomTextHandler) Enabled(ctx context.Context, level slog.Level) bool {
	return true
}

// Init - 로거 초기화
func Init(env string) {
	var handler slog.Handler

	if env == "production" {
		// 운영 환경: JSON 포맷
		handler = slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
			Level: slog.LevelInfo,
		})
	} else {
		// 개발 환경: Python과 동일한 텍스트 포맷
		handler = NewCustomTextHandler(os.Stdout)
	}

	logger := slog.New(handler)
	slog.SetDefault(logger)
}

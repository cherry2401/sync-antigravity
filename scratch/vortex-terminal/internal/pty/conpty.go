package pty

import (
	"context"
	"io"
	"os"
	"syscall"

	"github.com/charmbracelet/x/conpty"
	"github.com/google/uuid"
)

// Session represents a terminal session (Local or SSH)
type Session struct {
	ID     string
	ConPty *conpty.ConPty
	Stdin  io.Writer
	Stdout io.Reader
	Cancel context.CancelFunc
}

// NewLocalSession creates a new local PTY session
func NewLocalSession(shell string, rows, cols int) (*Session, error) {
	if shell == "" {
		shell = "powershell.exe"
	}

	cpty, err := conpty.New(cols, rows, 0)
	if err != nil {
		return nil, err
	}

	// Create ProcAttr with inherited environment variables
	attr := &syscall.ProcAttr{
		Env: os.Environ(),
	}

	// Spawn the shell process with environment
	_, _, err = cpty.Spawn(shell, nil, attr)
	if err != nil {
		cpty.Close()
		return nil, err
	}

	id := uuid.New().String()
	_, cancel := context.WithCancel(context.Background())

	return &Session{
		ID:     id,
		ConPty: cpty,
		Stdin:  cpty,
		Stdout: cpty,
		Cancel: cancel,
	}, nil
}

// Write sends data to the PTY
func (s *Session) Write(data []byte) error {
	_, err := s.Stdin.Write(data)
	return err
}

// Resize changes the terminal dimensions
func (s *Session) Resize(rows, cols int) error {
	return s.ConPty.Resize(cols, rows)
}

// Close terminates the session
func (s *Session) Close() error {
	if s.Cancel != nil {
		s.Cancel()
	}
	return s.ConPty.Close()
}

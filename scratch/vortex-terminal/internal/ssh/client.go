package ssh

import (
	"context"
	"fmt"
	"io"
	"time"

	"github.com/google/uuid"
	"golang.org/x/crypto/ssh"
)

type Session struct {
	ID      string
	Client  *ssh.Client
	Session *ssh.Session
	Stdin   io.WriteCloser
	Stdout  io.Reader
	Cancel  context.CancelFunc
}

func Connect(host, user, password string, port int, rows, cols int) (*Session, error) {
	config := &ssh.ClientConfig{
		User: user,
		Auth: []ssh.AuthMethod{
			ssh.Password(password),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), // For demo, should be more secure in production
		Timeout:         10 * time.Second,
	}

    addr := fmt.Sprintf("%s:%d", host, port)
	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		return nil, err
	}

	session, err := client.NewSession()
	if err != nil {
		client.Close()
		return nil, err
	}

	// Set up terminal modes
	modes := ssh.TerminalModes{
		ssh.ECHO:          1,     // enable echoing
		ssh.TTY_OP_ISPEED: 14400, // input speed = 14.4kbaud
		ssh.TTY_OP_OSPEED: 14400, // output speed = 14.4kbaud
	}

	// Request pseudo terminal
	if err := session.RequestPty("xterm-256color", rows, cols, modes); err != nil {
		session.Close()
		client.Close()
		return nil, err
	}

	stdout, err := session.StdoutPipe()
	if err != nil {
		session.Close()
		client.Close()
		return nil, err
	}

	stdin, err := session.StdinPipe()
	if err != nil {
		session.Close()
		client.Close()
		return nil, err
	}

	if err := session.Shell(); err != nil {
		session.Close()
		client.Close()
		return nil, err
	}

	_, cancel := context.WithCancel(context.Background())

	return &Session{
		ID:      uuid.New().String(),
		Client:  client,
		Session: session,
		Stdin:   stdin,
		Stdout:  stdout,
		Cancel:  cancel,
	}, nil
}

func (s *Session) Write(data []byte) error {
	_, err := s.Stdin.Write(data)
	return err
}

func (s *Session) Resize(rows, cols int) error {
	return s.Session.WindowChange(rows, cols)
}

func (s *Session) Close() error {
	if s.Cancel != nil {
		s.Cancel()
	}
	s.Session.Close()
	return s.Client.Close()
}

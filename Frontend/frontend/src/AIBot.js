import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './AIBot.css';
// import './Header-Logo.svg'
import Header from './Header';
function AIBot() {
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [urlErrorMessage, setUrlErrorMessage] = useState('');
    const [urlsuccessMessage, setUrlSuccessMessage] = useState('');

    const chatBottomRef = useRef(null);

    const handleFocus = () => {
        document.getElementById('urlInput').style.border = '2px solid #1366d6';
    };

    const handleBlur = () => {
        document.getElementById('urlInput').style.border = '0px solid transparent';
    };

    function handleLinkSubmit() {
        console.log("----", urlsuccessMessage);
        console.log("----", urlErrorMessage);
        const url = document.querySelector('input[type="text"]').value;
        const requestBody = {
            url: url
        };

        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
            .then(response => {
                if (!response.ok) {
                    setUrlSuccessMessage("")
                    setErrorMessage("URL Upload failed")

                    console.log("----a", urlsuccessMessage);
                    console.log("----a", urlErrorMessage);
                    throw new Error('Network response was not ok');
                }
            })
            .then(data => {
                setUrlSuccessMessage("URL Fetched Successfully")
                setErrorMessage("")

                console.log("----b", urlsuccessMessage);
                console.log("----b", urlErrorMessage);
                console.log('Response data:', data);
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
    }


    const handleMessageSend = async () => {
        if (inputText.trim() === '') return;

        const newMessage = {
            text: inputText,
            description: 'Me',
            sender: 'user'
        };

        // Update messages state with the new user message
        setMessages(prevMessages => [...prevMessages, newMessage]);
        setInputText('');

        try {
            const response = await axios.post('http://127.0.0.1:5000/chat', {
                question: inputText
            });

            const generatorMessage = {
                text: response.data.answer,
                description: 'Bot',
                sender: 'generator'
            };

            // Update messages state with the new generator message
            setMessages(prevMessages => [...prevMessages, generatorMessage]);
            setErrorMessage('');
        } catch (error) {
            setErrorMessage('Error: Failed to receive response'); // Set error message
            console.error('Error sending message:', error);
        }
    };

    useEffect(() => {
        if (chatBottomRef.current) {
            chatBottomRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages]);

    return (
        <div className="chat-bot">
            <Header />
            <div className="Chat-container">
                <div className="left-pane" style={{ width: '20%', height: '100%', backgroundColor: 'white', padding: '20px', boxSizing: 'border-box' }}>

                    <div className='input-card' style={{ flex: 1, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', boxSizing: 'border-box' }}>

                        {/* <div style={{ color: '#1f1f1f', fontSize: '1.0rem', fontWeight: 'bold', margin: '0px', paddingLeft: '5px', marginBottom: '10px' }}>
              <p>
                Enter URL
              </p>
            </div> */}

                        <div style={{ backgroundColor: '#f3f3f3', width: '95%', borderRadius: '8px', padding: '10px', textAlign: 'center', height: '120px' }}>
                            <input id="urlInput" type="text" placeholder="Enter URL here" style={{ fontSize: '16px', height: '35%', border: 'none', width: '100%', borderRadius: '5px', marginBottom: '15px', outline: 'none', borderBottom: '2px solid transparent', lineHeight: '100%', paddingLeft: '5px' }} onFocus={handleFocus} onBlur={handleBlur} />
                            <button style={{ height: '40%', fontSize: '16px', fontWeight: '500', borderRadius: '5px', backgroundColor: '#1366d6', color: 'white', border: 'none', padding: '0 20px', cursor: 'pointer', width: '100%' }} onClick={handleLinkSubmit}>Submit URL</button>
                        </div>


                        {urlsuccessMessage && <p style={{ color: 'green', marginTop: '10px' }}>{urlsuccessMessage}</p>}
                        {urlErrorMessage && <p style={{ color: 'red', marginTop: '10px' }}>{urlErrorMessage}</p>}

                    </div>

                </div>
                <div className='right-pane' style={{ width: '80%', height: '100%', backgroundColor: 'white', boxSizing: 'border-box', margin: '0px 10px', display: 'flex', flexDirection: 'column' }}>
                    <div className='clear'>
                        <div className="ClearChatButton">
                            <button onClick={() => setMessages([])}>Clear Chat</button>
                        </div>
                    </div>

                    <div className="Chat-interface">
                        <div className='head-mesage'>
                            <div className="Greeting">
                                <p style={{ margin: '0px', fontSize: '1rem', padding: '10px', color: '#fff', boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)', borderRadius: '8px', backgroundColor: '#1366d6' }}>Hello, I Am Your Web Data Analyzer Bot</p>
                            </div>
                            <div className="Greeting">
                                <p style={{ margin: '0px', fontSize: '1rem', padding: '10px', color: '#fff', boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)', borderRadius: '8px', backgroundColor: '#1366d6' }}>Uncover Insights, Empower Growth: Analyze Your Web Data </p>
                            </div>
                            <p className="sent-by-greet-info">Bot</p>
                        </div>

                        <div className="Chat-messages">
                            {messages.map((message, index) => (
                                <div className={`${message.sender}-message`}>
                                    <div className={`${message.sender}-message-wrap`}>
                                        <div key={index} className={`Message-${message.sender}`}>
                                            {message.sender === 'generator' ? (
                                                <>
                                                    {errorMessage ? (
                                                        <div> {errorMessage} </div>

                                                    ) : (
                                                        <div dangerouslySetInnerHTML={{ __html: message.text }} ></div>)
                                                    }
                                                </>
                                            ) : (
                                                <p style={{ margin: '0px' }}>{message.text}</p>
                                            )}
                                        </div>
                                    </div>
                                    <p className={`sent-by-${message.sender}-info`}>{message.description}</p>
                                </div>
                            ))}
                            <div ref={chatBottomRef} />
                        </div>
                    </div>
                    <div className="ChatInputArea">
                        <div className="Chat-input">
                            <input
                                type="text"
                                placeholder="Enter the description..."
                                value={inputText}
                                onChange={(e) => setInputText(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') {
                                        handleMessageSend();
                                    }
                                }}
                            />
                            <button onClick={handleMessageSend}>Send</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AIBot;

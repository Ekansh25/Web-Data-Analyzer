import React from 'react';
// import Logo from './image/Logo.svg'; // Import your logo image

function Header() {
    return (
        <header style={headerStyle}>
            <div style={containerStyle}>
                {/* <img src={Logo} alt="Logo" style={logoStyle} /> */}
                <h1 style={titleStyle}>Web Data Analyzer</h1>
            </div>
        </header>
    );
}

const headerStyle = {
    backgroundColor: '#1e1e1e',
    color: 'white',
    padding: '10px 20px',
    width: '100%',
    boxSizing: 'border-box',
};

const containerStyle = {
    display: 'flex',
    alignItems: 'center',
    // maxWidth: '900px', // Decrease the width as per your requirement
    margin: '0 auto',
};

const logoStyle = {
    width: 'auto',
    height: '100%',// Adjust the width of the logo as needed
    marginRight: '15px',
    marginLeft: '20px',
};

const titleStyle = {
    fontSize: '1.5rem',
    fontWeight: 'normal',
    margin: '0',
    fontFamily: 'system-ui',
    fontWeight: '500'
};

export default Header;
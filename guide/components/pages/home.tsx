import React from 'react';
import styles from './index.module.css';



const Main = () => {
    return (
        <main className={styles.main}>
            <h2>Dismake</h2>
            <p>Create serverless discord bots on top of FastAPI</p>
        </main>
    )
}

const HomePage = () => {
    return (
        <>
        <Main/>
        </>
    )
}


export default HomePage;
import {useEffect, useState} from "react";
import {Link} from "react-router-dom";

export const AboutPage = () => {
    const [content, set_content] = useState({});

    useEffect(() => {
        fetch('/about.json')
            .then((res) => res.json())
            .then((d) => set_content(d));
    }, []);

    return <div style={{
        padding: '10px',
        gap: '10px'
    }} className='base_flex_column'>
        <span>{content?.about}</span>
        <Link to='/debug' className='base_button desktop'>Нашли ошибку или есть предложение?</Link>
        <Link to='/debug' className='base_button mobile' style={{
            padding: '20px',
            marginTop: '15px',
        }}>Нашли ошибку или есть предложение?</Link>
    </div>
}
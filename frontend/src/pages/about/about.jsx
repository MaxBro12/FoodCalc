import {useEffect, useState} from "react";
import {Link, useSearchParams} from "react-router-dom";


export const AboutPage = () => {
    const [params] = useSearchParams();
    const [content, set_content] = useState({});
    const error = params.get('error') || undefined;

    useEffect(() => {
        fetch('/about.json')
            .then((res) => res.json())
            .then((d) => set_content(d));
    }, []);

    if (error === 'backend_off') {
        return <div>Не удалось подключиться к серверу. Пожалуйста, попробуйте позже.</div>;
    }
    if (error === 'inner') {
        return <div>Внутренняя ошибка приложения. Обратитесь к администратору.</div>;
    }

    return <div style={{
        padding: '10px',
        gap: '10px'
    }} className='base_flex_column'>
        <span>{content?.about}</span>
        <Link to='/about/feetback' className='base_button'>Нашли ошибку или есть предложение?</Link>
    </div>
}

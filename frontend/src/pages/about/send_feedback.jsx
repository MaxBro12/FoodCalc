import {useState} from "react";
import auth_service from "../../api/auth.jsx";
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";

export const DebugPage = () => {
    const [loading, set_loading] = useState(false);
    const [message, set_message] = useState('');

    const handle_msg = (e) => {
        e.preventDefault();
        set_message(e.target.value);
    }

    const handleSubmit = async () => {
        if (message.length === 0) {
            set_loading(true);
            await auth_service.send_feedback(message)
            set_loading(false);
        }
    }

    if (loading) {
        return <LoadingAnimation />
    }

    return <div className='base_flex_column' style={{
        marginTop: '5px',
        width: '100%',
    }}>
        <form onSubmit={handleSubmit} style={{
            width: '600px', alignItems: "center"
        }} className='base_flex_column'>
            <textarea value={message} onChange={(e) => handle_msg(e)}
                  placeholder='Как можно подробнее опишите проблему и её решение'
                  style={{
                      height: 200,
                      width: '100%',
                      border: "1px solid var(--border-color)",
                      backgroundColor: 'var(--button-color)',
                      color: 'var(--text-color)',
                      borderRadius: 10,
                      textAlign: 'left',
                      verticalAlign: 'top',
                      display: "block",
                      position: "relative",
                      marginLeft: "auto",
                      marginRight: "auto",
                      padding: "5px"
                  }}/>
            <input type="submit" className='base_button' style={{
                position: 'relative',
                right: 0,
                borderRadius: 10,
                /*margin: "5px 0px 0px auto",*/
                padding: "8px 16px"
            }}/>
        </form>
    </div>
}

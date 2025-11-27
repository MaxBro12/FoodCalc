import {useState} from "react";
import PropTypes from "prop-types";

const SettingsWindow = ({theme, set_theme}) => {
    const [small, set_small] = useState(true)

    return (
        <div className='settings-window-container'>
            {small ? <div className="settings-window-small">
                <span onClick={() => set_small(!small)}>настройки 🠉</span>
                </div>:
            <div className="settings-window-full">
                <span className='settings-window-small' onClick={() => set_small(!small)}>настройки 🠋</span>
                <div className='base_flex_column settings-window-full-container' style={{alignItems: "flex-start"}}>
                    <div className='base_flex_row' style={{justifyContent: 'space-between', width: '100%', flexWrap: 'nowrap'}}>
                        <label>Тема:</label>
                        <button style={{
                            width: "100%",
                            borderColor: 'var(--border-color)',
                            backgroundColor: theme === 'dark' ? 'white' : 'black',
                        }} onClick={() => set_theme(theme === 'dark' ? 'light': 'dark')}></button>
                    </div>
                </div>
            </div>}
        </div>
    )
}
SettingsWindow.propTypes = {
    theme: PropTypes.string.isRequired,
    set_theme: PropTypes.func.isRequired,
}
export default SettingsWindow;
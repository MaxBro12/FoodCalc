import { useState } from "react";
import { useDevice } from "@/context/mobile.jsx"


export const NewProduct = ({ on_close }) => {
    const {isMobile} = useDevice()

    const [formData, setFormData] = useState({
        id: '',
        name: '',
        description: '',
        calories_per_100: 0,
        proteins_per_100: 0,
        fats_per_100: 0,
        carbs_per_100g: 0,
        fiber_per_100g: 0,
        sugar_per_100g: 0,
        minerals: [],
    });

    const handleOuterClick = () => {
        on_close(false);
    };

    const handleInnerClick = (e) => {
        e.stopPropagation();
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const form_submit = async () => {
        if (formData.name !== '' && formData.status_url !== '') {
            await back_service.apps.new(formData)
        }
    }

    return <div className='overlay-backdrop' onClick={handleOuterClick}>
        <div className='overlay-content base_flex_column rounded_border' onClick={handleInnerClick} style={{
            minWidth: isMobile ? '85vw': '50vw',
            maxWidth: '90vw',
        }}>
            <NewAppForm formData={formData} form_submit={form_submit} handleChange={handleChange}/>
        </div>
    </div>
}

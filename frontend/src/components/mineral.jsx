import {mineral_color} from "../utils/minerals_colors.jsx";

export const Mineral = ({mineral}) => {
    return <div style={{
        border: `5px solid ${mineral_color(mineral.type_id).color}`,
        borderRadius: '10px',
        padding: '5px',
        color: mineral_color(mineral.type_id).color,
        backgroundColor: mineral_color(mineral.type_id).background,
        fontWeight: 'bolder',
        textAlign: 'center',
        verticalAlign: 'middle',
        userSelect: 'none',
        maxWidth: '300px',
        minWidth: '45px',
        height: '45px',
    }}>
        {mineral.name}
    </div>
}
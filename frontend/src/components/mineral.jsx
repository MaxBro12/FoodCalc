import {mineral_color} from "../utils/minerals_colors.jsx";

export const Mineral = ({mineral, spec_type_id = 1, compact = false, adt_str, progress, adt_style}) => {
    if (compact) {
        return <div className='mineral_base mineral_compact base_flex_column' style={{
            borderColor: mineral_color(mineral.type_id || spec_type_id).color,
            color: mineral_color(mineral.type_id || spec_type_id).color,
            backgroundColor: mineral_color(mineral.type_id || spec_type_id).background,
            height: adt_str ? '60px': '45px',
            width: adt_str ? '60px': '45px',
            flexWrap: 'nowrap',
        }}>
            <span style={{
                color: mineral_color(mineral.type_id || spec_type_id).color,
            }}>{mineral.compact_name}</span>
            {adt_str && <span style={{
                color: mineral_color(mineral.type_id || spec_type_id).color,
            }}>{adt_str}</span>}
        </div>
    }

    return <div className='mineral_base mineral_full base_flex_column' style={{
        borderColor: mineral_color(mineral.type_id || spec_type_id).color,
        backgroundColor: mineral_color(mineral.type_id || spec_type_id).background,
    }}>
        <span style={{
            color: mineral_color(mineral.type_id || spec_type_id).color,
        }}>{mineral.compact_name}</span>
        <span style={{
            color: mineral_color(mineral.type_id || spec_type_id).color,
        }}>{mineral.name}</span>
        {adt_str && <span style={{
            color: mineral_color(mineral.type_id || spec_type_id).color,
        }}>{adt_str}</span>}
    </div>
}
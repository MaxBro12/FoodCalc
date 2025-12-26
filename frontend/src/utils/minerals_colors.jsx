export function mineral_color(type_name) {
    switch (type_name) {
        case 'Водорастворимые':
            return {
                color: 'rgb(31,118,251)',
                background: 'rgba(13,126,255,0.29)',
            };
        case 'Жирорастворимые':
            return {
                color: 'rgb(251,229,0)',
                background: 'rgba(247,255,13,0.19)',
            };
        case 'Макронутриенты':
            return {
                color: 'rgb(31,118,251)',
                background: 'rgba(13,126,255,0.29)',
            };
        case 'Макроминералы':
            return {
                color: 'rgb(251,31,31)',
                background: 'rgba(255,13,13,0.29)',
            };
        case 'Микроминералы':
            return {
                color: 'rgb(54,193,7)',
                background: 'rgba(65,255,13,0.29)',
            };
        default:
            return {
                color: 'rgb(31,118,251)',
                background: 'rgba(13,126,255,0.29)',
            };
    }
}
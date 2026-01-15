export function mineral_color(type_name) {
    switch (type_name) {
        case 1: // Макронутриенты
            return {
                color: 'rgb(115,115,115)',
                background: 'rgba(131,131,131,0.21)',
            };
        case 2: // Водорастворимые
            return {
                color: 'rgb(31,118,251)',
                background: 'rgba(13,126,255,0.29)',
            };
        case 3: // Жирорастворимые
            return {
                color: 'rgb(255,196,0)',
                background: 'rgba(247,255,13,0.37)',
            };
        case 4: // Макроминералы
            return {
                color: 'rgb(251,31,31)',
                background: 'rgba(255,13,13,0.29)',
            };
        case 5: // Микроминералы
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
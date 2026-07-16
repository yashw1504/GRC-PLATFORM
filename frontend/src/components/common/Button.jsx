function Button({
    children,
    onClick,
    variant = "primary",
    type = "button",
    disabled = false
}) {

    const variants = {

        primary: {
            background: "#2563eb",
            color: "white"
        },

        success: {
            background: "#16a34a",
            color: "white"
        },

        danger: {
            background: "#dc2626",
            color: "white"
        },

        warning: {
            background: "#f59e0b",
            color: "#111827"
        },

        secondary: {
            background: "#334155",
            color: "white"
        }

    };

    return (

        <button

            type={type}

            disabled={disabled}

            onClick={onClick}

            style={{

                padding: "10px 18px",

                border: "none",

                borderRadius: "8px",

                cursor: disabled
                    ? "not-allowed"
                    : "pointer",

                fontWeight: 600,

                transition: ".2s",

                opacity: disabled ? .5 : 1,

                ...variants[variant]

            }}

        >

            {children}

        </button>

    );

}

export default Button;
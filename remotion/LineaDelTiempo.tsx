import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const LineaDelTiempo: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1b3a5c",
        justifyContent: "center",
        alignItems: "center",
        color: "white",
        fontFamily: "sans-serif",
        textAlign: "center",
      }}
    >
      <h1 style={{ fontSize: 80, opacity }}>
        TECNOLÓGICO DE ESTUDIOS SUPERIORES DE CHIMALHUACÁN
        <br />
        LÍNEA DEL TIEMPO
      </h1>
    </AbsoluteFill>
  );
};

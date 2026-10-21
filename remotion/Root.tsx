import { Composition } from "remotion";
import { LineaDelTiempo } from "./LineaDelTiempo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="LineaDelTiempo"
      component={LineaDelTiempo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};

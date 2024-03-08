import { animated, useSpring } from "@react-spring/web";

import DA from "../assets/A-D.png";
import D2 from "../assets/2-D.png";
import D3 from "../assets/3-D.png";
import D4 from "../assets/4-D.png";
import D5 from "../assets/5-D.png";
import D6 from "../assets/6-D.png";
import D7 from "../assets/7-D.png";
import D8 from "../assets/8-D.png";
import D9 from "../assets/9-D.png";
import D10 from "../assets/10-D.png";
import DJ from "../assets/J-D.png";
import DQ from "../assets/Q-D.png";
import DK from "../assets/K-D.png";

import HA from "../assets/A-H.png";
import H2 from "../assets/2-H.png";
import H3 from "../assets/3-H.png";
import H4 from "../assets/4-H.png";
import H5 from "../assets/5-H.png";
import H6 from "../assets/6-H.png";
import H7 from "../assets/7-H.png";
import H8 from "../assets/8-H.png";
import H9 from "../assets/9-H.png";
import H10 from "../assets/10-H.png";
import HJ from "../assets/J-H.png";
import HQ from "../assets/Q-H.png";
import HK from "../assets/K-H.png";

import CA from "../assets/A-C.png";
import C2 from "../assets/2-C.png";
import C3 from "../assets/3-C.png";
import C4 from "../assets/4-C.png";
import C5 from "../assets/5-C.png";
import C6 from "../assets/6-C.png";
import C7 from "../assets/7-C.png";
import C8 from "../assets/8-C.png";
import C9 from "../assets/9-C.png";
import C10 from "../assets/10-C.png";
import CJ from "../assets/J-C.png";
import CQ from "../assets/Q-C.png";
import CK from "../assets/K-C.png";

import SA from "../assets/A-S.png";
import S2 from "../assets/2-S.png";
import S3 from "../assets/3-S.png";
import S4 from "../assets/4-S.png";
import S5 from "../assets/5-S.png";
import S6 from "../assets/6-S.png";
import S7 from "../assets/7-S.png";
import S8 from "../assets/8-S.png";
import S9 from "../assets/9-S.png";
import S10 from "../assets/10-S.png";
import SJ from "../assets/J-S.png";
import SQ from "../assets/Q-S.png";
import SK from "../assets/K-S.png";

import cardBack from "../assets/cardBack.png";

const cardAssetPath: Record<string, string> = {
  "A-C": CA,
  "2-C": C2,
  "3-C": C3,
  "4-C": C4,
  "5-C": C5,
  "6-C": C6,
  "7-C": C7,
  "8-C": C8,
  "9-C": C9,
  "10-C": C10,
  "J-C": CJ,
  "Q-C": CQ,
  "K-C": CK,
  "A-D": DA,
  "2-D": D2,
  "3-D": D3,
  "4-D": D4,
  "5-D": D5,
  "6-D": D6,
  "7-D": D7,
  "8-D": D8,
  "9-D": D9,
  "10-D": D10,
  "J-D": DJ,
  "Q-D": DQ,
  "K-D": DK,
  "A-S": SA,
  "2-S": S2,
  "3-S": S3,
  "4-S": S4,
  "5-S": S5,
  "6-S": S6,
  "7-S": S7,
  "8-S": S8,
  "9-S": S9,
  "10-S": S10,
  "J-S": SJ,
  "Q-S": SQ,
  "K-S": SK,
  "A-H": HA,
  "2-H": H2,
  "3-H": H3,
  "4-H": H4,
  "5-H": H5,
  "6-H": H6,
  "7-H": H7,
  "8-H": H8,
  "9-H": H9,
  "10-H": H10,
  "J-H": HJ,
  "Q-H": HQ,
  "K-H": HK,
};

export function Card({
  card,
  showBack = false,
}: {
  card: string;
  showBack?: boolean;
}) {
  const springs = useSpring({
    from: { x: 0 },
    to: { x: 10 },
  });

  const assetPath = showBack ? cardBack : cardAssetPath[card];
  return (
    <animated.img
      src={assetPath}
      style={{ height: 168, width: 113, ...springs }}
    />
  );
}

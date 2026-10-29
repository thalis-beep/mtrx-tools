"""V2 revisions: Hook 1 without laundry + locked couch coverage (wide / mom single / daughter single)."""
import json, sys
from build_requests import MOM_V, DAU_V, DRAMA, END, request

# Locked first frames
H1, H2, H3, H4 = ("5323dd1e-c935-4186-a9d8-38aa9b71c328", "94c7bb08-dd90-44c9-9cd5-6f0e30b9bc8c",
                  "9a971dde-b168-4cc9-86f2-138cb09361ea", "f417adc1-85dd-40e7-a605-fb782cbb3145")
WIDE_A, WIDE_B = "87d8806b-fa3c-4a09-bbc7-21676b17ffa1", "99544d2f-888b-4f1d-b27b-d18bd92c0bdd"
MOM_A, MOM_B = "06c4c6fd-dd4d-415b-bd0f-a25ef481c77f", "ec2483a4-c8dc-47f5-bd99-f1e2eebe0b6a"
DAU_A, DAU_B = "c97918d6-9108-4e31-b066-74a54d334e45", "0e999eab-1ee4-4507-b56b-3d93cd7ff7ba"

ONE = "She is the only person in the frame; no other people, shoulders or hands ever appear."
TWO = "Only the mother (left) and the daughter (right) are in the frame; nobody else ever appears."
MOM_EYE = "Her eyes stay slightly to the right of camera, on her daughter sitting off-frame to the right."
DAU_EYE = "Her eyes stay slightly to the left of camera, on her mother sitting off-frame to the left."
STATIC = "Locked-off camera, same framing for the whole shot, no cuts."

SHOTS = [
 ("h1", H1, 6, "Evening, warm sconce light. The older woman, empty-handed, climbs the carpeted stairs away from camera, one hand on the handrail. Her foot catches a step, she stumbles forward and falls heavily to her knees on the stairs, catching herself with both hands on the steps. She stays there on her knees, shaken. Static low angle, subtle handheld shake on the fall. Audio: slow footsteps on carpet, a thud as her knees hit the stairs, a sharp gasp, quiet house room tone. Nothing else on the stairs. No dialogue, no music, no subtitles."),
 ("h2", H2, 4, f"Evening. The older woman kneels on the stairs, gripping the handrail, catching her breath, eyes down on the step, and mutters under her breath to herself, not to anyone: \"These stairs are getting harder lately...\" {MOM_V}, soft, low, tired. {ONE} Slow subtle push-in. Shaky breath, room tone. {DRAMA} {END}"),
 ("h3", H3, 4, f"Evening. The young woman with the dish towel on her shoulder hurries out of the kitchen toward the stairs, her eyes locked up on her mother on the staircase off-frame to the right, and calls out: \"Mom! Are you okay?\" {DAU_V}, urgent and scared. {ONE} Handheld follow. Quick footsteps on hardwood. The floor stays clean. {DRAMA} {END}"),
 ("h4", H4, 4, f"Evening, close-up. Still kneeling on the stairs with her hand on the handrail, the older woman looks down toward her daughter at the bottom of the stairs off-frame, forces a small embarrassed smile and says: \"I'm fine, I'm fine. Just lost my footing.\" {MOM_V}, light and dismissive. {ONE} Her eyes stay down toward the bottom of the stairs. {STATIC} {DRAMA} {END}"),
 ("12", MOM_A, 6, f"The mother, tired and vulnerable, searching for words, admits to her daughter: \"I don't know how to explain it. I just feel weak. And my mind isn't sharp like it used to be.\" {MOM_V}, hesitant pauses. {MOM_EYE} {ONE} {STATIC} {DRAMA} {END}"),
 ("13", WIDE_A, 8, f"Wide two-shot on the sofa. The mother, eyes lowered to her clasped hands, confesses quietly while her daughter listens, holding her hand: \"I feel foggy, slow, like I'm half a step behind everything. It's like I'm not really myself anymore.\" {MOM_V}, voice cracking slightly. The daughter does not speak. {TWO} {STATIC} {DRAMA} {END}"),
 ("15", MOM_A, 6, f"A tear on the mother's cheek, chin trembling, pride and fear: \"I didn't want you to worry. I didn't want to be the mom you have to take care of.\" {MOM_V}, emotional, near tears. {MOM_EYE} {ONE} {STATIC} {DRAMA} {END}"),
 ("16", DAU_A, 6, f"The daughter's worry softens into a warm, reassuring small smile: \"Mom, please. If you'd told me sooner, you could've been feeling so much better by now.\" {DAU_V}, gentle, mood lifting. {DAU_EYE} {ONE} {STATIC} {DRAMA} {END}"),
 ("17", MOM_A, 4, f"The mother wipes a tear and lifts her eyes, a flicker of hope: \"What do you mean?\" {MOM_V}, curious, hopeful. {MOM_EYE} {ONE} {STATIC} {DRAMA} {END}"),
 ("18", WIDE_B, 8, f"Wide two-shot on the sofa. The daughter, the Nectar pouch on her lap, hands the Nectar stick pack to her mother and says to her: \"Try this. It's Nectar Creatine. You're going to take one of these every morning with a glass of water.\" {DAU_V}, warm, matter-of-fact. The mother takes the stick pack and looks at it. Packaging designs never change. {TWO} {STATIC} {DRAMA} {END}"),
 ("19", MOM_B, 4, f"The mother holds up the Nectar stick pack, label to camera, frowning skeptically: \"Creatine? Why on earth would I take creatine?\" {MOM_V}, skeptical, half-amused. {MOM_EYE} The stick pack design never changes and stays in her hand. {ONE} {STATIC} {DRAMA} {END}"),
 ("20a", DAU_B, 8, f"The daughter, holding the Nectar pouch, explains patiently: \"Because after forty, your body runs low on it, and creatine is what your cells use to make ATP.\" {DAU_V}, clear, caring. {DAU_EYE} The pouch stays in her hands, design unchanged. {ONE} {STATIC} {DRAMA} {END}"),
 ("20b", WIDE_B, 8, f"Wide two-shot on the sofa. The daughter, holding the Nectar pouch, keeps explaining to her mother, who holds the stick pack and listens: \"It's literally the fuel your muscles and your brain run on. Women barely have any to begin with, so you need to get your levels back up.\" {DAU_V}. The mother does not speak. Packaging designs never change. {TWO} {STATIC} {DRAMA} {END}"),
 ("21", MOM_B, 8, f"The mother, holding the Nectar stick pack, doubtful: \"I don't know, honey. Every mom I know has told me creatine's done nothing for them. They just get bloated and give up after a week.\" {MOM_V}, skeptical, grounded. {MOM_EYE} The stick pack stays in her hand. {ONE} {STATIC} {DRAMA} {END}"),
 ("22a", DAU_B, 8, f"The daughter, holding the Nectar pouch with the label to camera, smiles reassuringly: \"Because they're not taking good quality stuff, Mom. Most creatine is packed with artificial fillers your body can't absorb.\" {DAU_V}, warm, confident. {DAU_EYE} The pouch stays in her hands, design unchanged. {ONE} {STATIC} {DRAMA} {END}"),
 ("22b", WIDE_B, 8, f"Wide two-shot on the sofa. The daughter lifts the Nectar pouch a little toward her mother and says, upbeat and sure: \"Nectar is clean. Zero sugar, zero calories, non-GMO, plant-based, and keto and paleo friendly.\" {DAU_V}. The mother listens. Packaging designs never change. {TWO} {STATIC} {DRAMA} {END}"),
 ("24", MOM_B, 4, f"The mother looks down at the stick pack in her hand, then back up, and gives a small, unsure nod with a faint smile: \"...Alright. I'll give it a shot.\" {MOM_V}, hesitant, willing. {MOM_EYE} {ONE} {STATIC} {DRAMA} {END}"),
]

if __name__ == "__main__":
    want = set(sys.argv[1:])
    reqs = [request(i, *s) for i, s in enumerate(SHOTS) if not want or s[0] in want]
    print(json.dumps(reqs))
    print(f"# clips={len(reqs)} seconds={sum(r['params']['duration'] for r in reqs)}", file=sys.stderr)

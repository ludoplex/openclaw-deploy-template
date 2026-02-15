

---

# 17. BOSS BATTLES RULES (2nd Edition)

> **Source:** Ward Rules Guide Boss Battles 2nd Edition
> **Effective Date:** January 9th, 2026
> **Authority:** Ward Trading Card Company LLC

## 17.1 Overview

Boss Battles are a cooperative game mode where one or more players face a powerful Boss creature controlled by automated rules. The Boss plays by its own rules and is designed to create high-pressure, raid-style gameplay.

**Victory:** Players win when Boss HP reaches 0.
**Defeat:** Boss wins when all players are eliminated.

## 17.2 Player Elimination

A player is eliminated when:
- Cemetery reaches 300+ HP, OR
- No playable creatures remain in deck or hand

Once eliminated:
- Player is permanently out
- Cannot re-enter for any reason
- All cards under their control are removed from the game

## 17.3 Turn Structure

### Turn Pattern (Multi-Player)
Boss then Player 1 then Boss Mini Turn then Player 2 then Boss Mini Turn then Player 3 then Boss

### Turn Pattern (Solo)
Boss then Player then Boss (no Mini Turns)

### Boss Primary Turn
1. Draw Phase
2. Play Magic Phase
3. Combat Phase (Boss ALWAYS attacks)

### Boss Mini Turn (between player turns)
- Draw 1 card
- Play immediately
- If card cannot logically resolve, discard with no effect

## 17.4 Boss Restrictions and Immunities

### Cannot Be Removed
- Cannot leave field except by death
- Cannot be returned to hand or deck
- Cannot be banished, swapped, or replaced

### Damage Immunities
- Immune to percentage-based damage
- Immune to fractional HP reduction
- Only Attack Damage and effect damage allowed

### Deck Rules
- Boss never has a hand (cards immediately resolved)
- Maximum 5 Infinite Magic cards on field
- Extra Infinite cards discarded with no effect
- When deck empties, shuffle cemetery, reset deck (never runs out)

## 17.5 Boss Resistance Mechanic

### Magic Cards vs Boss
| Roll | Result |
|------|--------|
| 4-6 | Effect succeeds |
| 1-3 | Effect resisted, card sent to player cemetery |

### Creature Effects vs Boss
- Same 4-6 requirement
- Each effect may only attempt once per turn (unless card states otherwise)
- Failed creature effects do NOT send creature to cemetery

### When Resistance Roll Required
- Any Magic/effect that directly affects Boss stats, attack order, or combat outcome
- Examples requiring roll: Absolute Terror on Boss, Junk Scarecrow blocking Boss attack, Backstab (alters combat timing)
- Examples NOT requiring roll: Dragon Power on your own creature

## 17.6 Boss Attack Rules

- Boss ALWAYS attacks on its turn
- Boss only attacks primary creatures (unless stated otherwise)

### Target Selection
1. Each player rolls a die
2. Lowest roll is targeted
3. Reroll ties until resolved

## 17.7 Boss Magic Targeting

1. Each player rolls a die
2. Lowest roll equals targeted player
3. If multiple valid cards: targeted player assigns numbers, die roll determines specific target

## 17.8 Magic Chains and Lightning

No changes from standard Ward rules:
- One card per response
- Effects resolve in reverse order
- Lightning timing unchanged
- Team size does NOT increase response capacity

## 17.9 Break Free (Special Boss Card)

**Break Free** cannot be negated or stopped once drawn.
- Immediately removes ALL player creature/magic effects from Boss
- Plays even if Boss is under effect preventing Magic play
- Essentially resets the Boss to clean state

## 17.10 Intelligence Rule

When ambiguity arises: **Boss always performs the smartest possible action.**

Ask: "What would the Boss do if it were trying to win?"

Includes:
- Choosing optimal targets
- Avoiding negative effects when possible
- Prioritizing survival or lethal pressure

## 17.11 Simulator Implementation Notes

### Boss State Machine
- Track Boss HP, field (primary only plus magic slots), cemetery
- No hand state needed
- Deck reshuffles from cemetery when empty

### Turn Automation
- Boss draws then immediate resolution
- Target selection via die roll simulation (lowest of N dice)
- Resistance checks (4-6 success) for player effects targeting Boss

### Combat Differences
- Boss always attacks (no choice)
- Boss only targets primary creatures
- Players roll to determine target

### Special Cards
- Implement Break Free as unblockable effect clear
- Track which effects have attempted Boss resistance this turn

---

**Document Version:** 1.2
**Generated:** 2026-02-13
**Updated:** Added Boss Battles Rules (Section 17)
**For:** WARD TCG Simulator Implementation

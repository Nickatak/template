# Feature Map: Demo Feature

## Purpose
Demonstrate the routing shim pattern: route files mount a parent feature component, while flow logic stays in feature-level components/hooks.

## Route Surface
1. `/demo-feature`

## Mutation Map
1. `DemoSubmission`
   - create in local feature state (client-only demo submit)

## Composition and Entry Flow
1. Entry sources:
   - direct route entry: `app/demo-feature/page.tsx` mounts `DemoFeatureConsole`
   - feature export entry: `features/demo-feature/index.ts` exports `DemoFeatureConsole`
2. Parent/Owner:
   `DemoFeatureConsole` owns composition and wires controller state/actions into child components.
3. Controller/Hook:
   `useDemoFeatureController` owns form state, validation, submit handling, and status messaging.
4. Children:
   `DemoFeatureForm` renders inputs and emits submit/change callbacks.
5. Default behavior:
   render form, collect inputs, and submit into local controller state.
6. Overrides:
   validation failures return inline field errors and block submission.
7. Relationship flow:
   route mount -> console render -> child submit -> controller state mutation -> console re-render.

## API Surface Used
1. none (client-only demo):
   this feature intentionally avoids backend integration and demonstrates composition boundaries only.

## Backend Contracts Used
- Contract endpoint(s): none
- Consumed fields: none
- Behavior source: local controller logic in `features/demo-feature/hooks/use-demo-feature-controller.ts`
- Fallback policy: n/a (no contract adapter in this feature)

## State Model (Remote, Local, Derived)
- State buckets:
  - Remote Data:
    - none
  - Local UI State:
    - title input
    - details input
    - field errors
    - status message
    - last submission
  - Derived State:
    - submission allowed/blocked by validation result

## Error and Empty States
- Error states:
  - required title validation error
- Empty states:
  - no last submission yet

## Test Anchors
- Existing anchors:
  - none
- TODO:
  - add controller validation tests
  - add form interaction tests
  - add route shim composition test (`app/demo-feature/page.tsx` mounts feature parent)

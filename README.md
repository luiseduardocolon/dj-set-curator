# DJ Set Curator

**AI-powered harmonic mixing engine for DJs**

## Vision
Automatically generate optimized DJ sets using:
- Harmonic key compatibility (Camelot wheel)
- BPM matching
- Energy progression
- Strategic crowd engagement (popularity-weighted peak placement)

## Project Status
🚧 **In Development** - Building incrementally

This project is being developed as a demonstration of:
1. Multi-step API orchestration
2. Durable workflow execution with Temporal
3. Real-world music industry data integration

## Roadmap
- [ ] Data collection (Spotify API integration)
- [ ] Harmonic analysis (Camelot wheel implementation)
- [ ] Set sequencing algorithm
- [ ] Temporal workflow migration
- [ ] Full explainability (transition justifications)

## Follow Along
Check commit history to see incremental development process!

## License
MIT


## Dataset

After encountering API restrictions on February 11, 2026 (Spotify lockdown, GetSongBPM approval requirements), this project uses a curated dataset to focus on the core algorithmic innovation.

The dataset (`tracks_dataset.json`) includes 20 popular tracks with verified:
- BPM (tempo)
- Musical key and mode
- Energy and danceability metrics
- Popularity scores

This approach prioritizes:
- **Reliability**: No API failures during demos
- **Reproducibility**: Consistent results
- **Focus**: Algorithm development over API integration
- **Performance**: No rate limiting delays

The multi-source API fetcher code remains in the repository as proof of concept.
